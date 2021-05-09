import setuptools

setuptools.setup(
    name="textractor",
    author="Samuel Rochette",
    author_email="samuel.rochette06@gmail.com",
    description="Misc AI projects",
    long_description=open("README.md").read(),
    url="https://github.com/Saxamos/textractor",
    entry_points={"console_scripts": ["prospectus = prospectus_field_extraction.__main__:main"]},
)
