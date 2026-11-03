"""Version identity from decoded Android manifests; missing values stay None."""
from dataclasses import asdict, dataclass
import xml.etree.ElementTree as ET

ANDROID = '{http://schemas.android.com/apk/res/android}'


class AnalysisError(ValueError):
    """Unusable or unsafe analysis input."""


@dataclass(frozen=True)
class ApkIdentity:
    package: str | None
    version_name: str | None
    version_code: int | None
    min_sdk: str | None
    target_sdk: str | None
    compile_sdk: str | None
    compile_codename: str | None

    def to_dict(self):
        return asdict(self)


def parse_manifest(text):
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise AnalysisError('Manifest XML declarations/entities are not allowed')
    try:
        root = ET.fromstring(text)
        if root.tag != 'manifest':
            raise AnalysisError('Expected a manifest root')
        attr = lambda element, name: element.get(ANDROID + name) if element is not None else None
        sdk = root.find('uses-sdk')
        low = attr(root, 'versionCode')
        major = attr(root, 'versionCodeMajor')
        code = ((int(major or '0') << 32) | int(low)) if low is not None else None
        if code is not None and (code < 0 or int(low) > 0xffffffff or int(major or '0') < 0):
            raise AnalysisError('Invalid version code')
        identity = ApkIdentity(root.get('package'), attr(root, 'versionName'), code,
            attr(sdk, 'minSdkVersion'), attr(sdk, 'targetSdkVersion'),
            attr(root, 'compileSdkVersion'), attr(root, 'compileSdkVersionCodename'))
        app = root.find('application')
        permissions = [dict(e.attrib) for e in root if e.tag in {'uses-permission', 'uses-permission-sdk-23'}]
        features = [dict(e.attrib) for e in root.findall('uses-feature')]
        metadata = [dict(e.attrib) for e in app.findall('meta-data')] if app is not None else []
        split = {
            'split_name': root.get('split'),
            'is_split_required': attr(app, 'isSplitRequired'),
            'required_split_types': attr(root, 'requiredSplitTypes'),
            'split_types': attr(root, 'splitTypes'),
            'uses_splits': [dict(e.attrib) for e in root.findall('uses-split')],
            'application_metadata': metadata,
        }
        return {'identity': identity.to_dict(), 'permissions': permissions,
                'declared_features': features, 'split_indicators': split,
                'application_attributes': dict(app.attrib) if app is not None else {}}
    except (ET.ParseError, ValueError) as exc:
        if isinstance(exc, AnalysisError): raise
        raise AnalysisError(f'Invalid decoded manifest: {exc}') from exc
