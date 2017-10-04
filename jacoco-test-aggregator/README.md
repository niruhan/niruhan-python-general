-------------------------------
FUNCTION OF THE SCRIPT
-------------------------------
This python script will;

1. Go through all the components recursively and scan for all the poms that have "bundle" packaging
2. It will extract the groupId, artifactId, version of the bundle packaged poms and create a new component
called coverage-reports and auto generate the required pom
3. modify the parent pom in the following ways
	1. add the coverage-reports module
	2. add the correct jacoco version
	3. if surefire and jacoco plugins are available will remove them
	4. add the correct surefire and jacoco versions with required tags to generate aggregate coverage

---------------------------
USAGE INSTRUCTIONS
---------------------------

1. For the directory variable replace the "/home/niruhan/test hackathon/carbon-analytics/carbon-analytics" with the home directory of your project
2. Since this script will modify the surefire and jacoco plugins in parent pom make a backup copy of the parent pom if required.
3. run the script (python 3.2 or above)
4. build the project using maven. Code coverage reports will be generated in the coverage-reports component
