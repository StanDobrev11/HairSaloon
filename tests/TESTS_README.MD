1. Best practice when creating tests is to follow dir structures as flws:

- create 'tests' package where templates folder is located;
- create 'app_name' package inside the 'tests' package to mach the app in the project
- create 'views' package to include .py files to tests the view and so on

2. It is good practice for each view to have separate file, not all views to be included in same .py file