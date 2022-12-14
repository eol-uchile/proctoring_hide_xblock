"""Setup for eolconditional XBlock."""



import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='proctoring-hide-xblock',
    version='0.1',
    description='.',
    license='AGPL v3',
    packages=[
        'proctoring_hide',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'proctoring_hide = proctoring_hide:ProctoringHideXBlock',
        ],
        "lms.djangoapp": [
            "proctoring_hide = proctoring_hide.apps:ProctoringHideConfig",
        ],
        "cms.djangoapp": [
            "proctoring_hide = proctoring_hide.apps:ProctoringHideConfig",
        ]
    },
    package_data=package_data("proctoring_hide", ["static", "public"]),
)
