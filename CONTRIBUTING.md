Development procedure
===

 - `master` branch is from where the production site is being deployed. We never push to `master` unless it's a hotfix.
 - We create feature branches for any feature we work on. Once you're done working on the feature branch, send a Pull Request to the `develop` branch. Others will review your code and comment. You can make changes and push commits to the same PR.
 - Once everything looks fine we merge the feature branch PR to the `develop` branch. You should then delete the feature branch.
 - Once we have the `develop` branch ready for deployment, we make a PR to the `master` branch. Once the code is reviewed, we merge it to `master` and deploy it.

Conventions
===

 - For the Python part, we follow pep8 in most cases. We use [`flake8`](http://flake8.readthedocs.org/en/latest/) to check for linting errors. Once you're ready to commit changes, check your code with `flake8` with this command -

        flake8 --max-complexity=24 --statistics --benchmark --ignore=E5,F4 <project_dir>/

 If there is any error, fix it and then commit.

 - For the Django part, we follow standard [Django coding style](https://docs.djangoproject.com/en/1.7/internals/contributing/writing-code/coding-style/).

 - If you are changing/creating any model, use `./manage.py makemigrations <appname>` to generate the migrations. Send PR. Let other's review the models.

 - And always remember the Zen.
