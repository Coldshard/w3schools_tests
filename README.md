# w3schools_tests
 Selenium tests for w3schools SQL module

- Tests are realized in Chrome browser only, because geckodriver doesn't work properly on this site.
- Browser is implemented through conftest fixture.
- All selectors are in the separate file, they are transfered as unpackable tuple of (type,code).
- All the tests are in the same class, they are using general setup. Page object pattern is used.
- Because there are no different pages for test, BasePage for inheritance is not realized.
- All the tests are marked with code "t" + test №, e.g. "t3 is for test #3". This is done for quick selective launch using marks through pytest -m.
- Project files successfully passed flake8 linter.
- Dependencies are in requirements.txt
- Code is documented using docstrings