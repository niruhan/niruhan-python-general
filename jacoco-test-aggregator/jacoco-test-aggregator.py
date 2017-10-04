import xml.etree.ElementTree as ET
import re
import os
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

#set this to the home directory of your project
directory = "/home/niruhan/test hackathon/carbon-analytics/carbon-analytics"
#IMPORTANT
#This script will remove the surefire and jacoco plugins from parent pom and add the required
#versions and tags of the surefire and jacoco plugins into parent pom. So make a copy of the
#parent pom if u want to save the plugins

#handling parent pom
with open(os.path.join(directory, "pom.xml")) as f:
    parentPom = f.read()

parentPom = re.sub('\\sxmlns="[^"]+"', '', parentPom, count=1)
parentPomRoot = ET.fromstring(parentPom)
parentModules = parentPomRoot.find("modules")
ET.SubElement(parentModules, "module").text = "coverage-reports"
parentPomProperties = parentPomRoot.find("properties")
parentPomJacocoVersion = parentPomProperties.findall("org.jacoco.version")
if (len(parentPomJacocoVersion) == 0):
    ET.SubElement(parentPomProperties, "org.jacoco.version").text = "0.7.9"
else:
    parentPomJacocoVersion[0].text = "0.7.9"

parentPomBuild = parentPomRoot.find("build")

if (len(parentPomBuild.findall("plugins")) > 0):
    buildPlugins = parentPomBuild.find("plugins")
    buildPluginsList = buildPlugins.findall("plugin")
    # print(buildPluginsList)
    for plugin in buildPluginsList:
        if (plugin.find("artifactId").text == "maven-surefire-plugin"):
            buildPlugins.remove(plugin)
        if (plugin.find("artifactId").text == "jacoco-maven-plugin"):
            buildPlugins.remove(plugin)
else:
    buildPlugins = ET.SubElement(parentPomBuild, "plugins")

# adding surefire plugin
surefirePlugin = ET.SubElement(buildPlugins, "plugin")
ET.SubElement(surefirePlugin, "groupId").text = "org.apache.maven.plugins"
ET.SubElement(surefirePlugin, "artifactId").text = "maven-surefire-plugin"
ET.SubElement(surefirePlugin, "version").text = "2.4.3"
surefireConfigs = ET.SubElement(surefirePlugin, "configuration")
ET.SubElement(surefireConfigs, "testSourceDirectory").text = "${project.build.testSourceDirectory}"
ET.SubElement(surefireConfigs, "testClassesDirectory").text = "${project.build.testOutputDirectory}"
surefireIncludes = ET.SubElement(surefireConfigs, "includes")
ET.SubElement(surefireIncludes, "include").text = "**/*TestCase.java"
ET.SubElement(surefireIncludes, "include").text = "**/*Test.java"
ET.SubElement(surefireConfigs, "useFile").text = "false"
ET.SubElement(surefireConfigs, "forkMode").text = "once"

# adding jacoco plugin
JacocoPlugin = ET.SubElement(buildPlugins, "plugin")
ET.SubElement(JacocoPlugin, "groupId").text = "org.jacoco"
ET.SubElement(JacocoPlugin, "artifactId").text = "jacoco-maven-plugin"
ET.SubElement(JacocoPlugin, "version").text = "${org.jacoco.version}"
newJacocoExecutions = ET.SubElement(JacocoPlugin, "executions")

newjacocoExecution = ET.SubElement(newJacocoExecutions, "execution")
ET.SubElement(newjacocoExecution, "id").text = "jacoco-initialize"
goals = ET.SubElement(newjacocoExecution, "goals")
ET.SubElement(goals, "goal").text = "prepare-agent"

newjacocoExecution = ET.SubElement(newJacocoExecutions, "execution")
ET.SubElement(newjacocoExecution, "id").text = "jacoco-site"
ET.SubElement(newjacocoExecution, "phase").text = "post-integration-test"
goals = ET.SubElement(newjacocoExecution, "goals")
ET.SubElement(goals, "goal").text = "report"
configuration = ET.SubElement(newjacocoExecution, "configuration")
excludes = ET.SubElement(configuration, "excludes")
ET.SubElement(excludes, "exclude").text = "**/SiddhiQLBaseVisitor.class"
ET.SubElement(excludes, "exclude").text = "**/SiddhiQLParser*"
ET.SubElement(excludes, "exclude").text = "**/SiddhiQLLexer*"


tree = ET.ElementTree(parentPomRoot)
tree.write(os.path.join(directory, "pom.xml"))

#building a new code-coverage pom
newRoot = ET.Element("project", xmlns="http://maven.apache.org/POM/4.0.0")
newRoot.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
newRoot.set('xsi:schemaLocation', "http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd")
newParent = ET.SubElement(newRoot, "parent")

ET.SubElement(newParent, "groupId").text = parentPomRoot.find("groupId").text
ET.SubElement(newParent, "artifactId").text = parentPomRoot.find("artifactId").text
ET.SubElement(newParent, "version").text = parentPomRoot.find("version").text
ET.SubElement(newParent, "relativePath").text = "../pom.xml"

ET.SubElement(newRoot, "modelVersion").text = parentPomRoot.find("modelVersion").text
ET.SubElement(newRoot, "artifactId").text = "coverage-reports"
ET.SubElement(newRoot, "packaging").text = "pom"
newDependencies = ET.SubElement(newRoot, "dependencies")

tree = ET.ElementTree(newRoot)

for root2, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith("pom.xml"):
            with open(os.path.join(root2, file)) as f:
                xmlstring = f.read()

            xmlstring = re.sub('\\sxmlns="[^"]+"', '', xmlstring, count=1)
            root = ET.fromstring(xmlstring)
            if (len(root.findall('packaging')) != 0):
                # print(root.findall('packaging')[0].text)
                if (root.find('packaging').text == "bundle"):
                    parent = root.find('parent')

                    groupID = parent.find('groupId').text
                    artifactID = root.find('artifactId').text

                    if(artifactID.endswith(".stub")):
                        break

                    if (len(root.findall('version')) >0 ):
                        version = root.find('version').text
                    else:
                        version = parent.find('version').text

                    currentDependency = ET.SubElement(newDependencies, "dependency")
                    ET.SubElement(currentDependency, "groupId").text = groupID
                    ET.SubElement(currentDependency, "artifactId").text = artifactID
                    ET.SubElement(currentDependency, "version").text = version

newBuild = ET.SubElement(newRoot, "build")
ET.SubElement(newBuild, "sourceDirectory").text = "src"
newPlugins = ET.SubElement(newBuild, "plugins")
newJacocoPlugin = ET.SubElement(newPlugins, "plugin")
ET.SubElement(newJacocoPlugin, "groupId").text = "org.jacoco"
ET.SubElement(newJacocoPlugin, "artifactId").text = "jacoco-maven-plugin"
ET.SubElement(newJacocoPlugin, "version").text = "${org.jacoco.version}"
newJacocoExecutions = ET.SubElement(newJacocoPlugin, "executions")
newjacocoExecution = ET.SubElement(newJacocoExecutions, "execution")
ET.SubElement(newjacocoExecution, "id").text = "report-aggregate"
ET.SubElement(newjacocoExecution, "phase").text = "prepare-package"
goals = ET.SubElement(newjacocoExecution, "goals")
ET.SubElement(goals, "goal").text = "report-aggregate"
configuration = ET.SubElement(newjacocoExecution, "configuration")
ET.SubElement(configuration, "title").text = "Test Coverage"
ET.SubElement(configuration, "footer").text = "Code Coverage Report"
includes = ET.SubElement(configuration, "includes")
ET.SubElement(includes, "include").text = "**/*.class"
excludes = ET.SubElement(configuration, "excludes")
ET.SubElement(excludes, "exclude").text = "**/*Constants.class"
ET.SubElement(excludes, "exclude").text = "**/*Exception.class"

os.makedirs(os.path.join(directory, "coverage-reports"), exist_ok=True)

file = open(os.path.join(directory, "coverage-reports", "pom.xml"), "w")
file.write(prettify(newRoot))
file.close()

print(prettify(newRoot))
