This python script will;

1. Go through all the components recursively and scan for all the poms that have "bundle" packaging
2. It will extract the groupId, artifactId, version of the bundle packaged poms and create a new component
	called coverage-reports and auto generate the required pom
3. modify the parent pom in the following ways
	1. add the coverage-reports module
	2. add the correct jacoco version
	3. if surefire and jacoco plugins are available will remove them
	4. add the correct surefire and jacoco versions with required tags to generate aggregate coverage
