import click
from functools import reduce
import os
import subprocess

"""
Convenience function to execute the given command in an interactive bash
"""
def runCommand(command):    
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        # returns None while subprocess is running
        retcode = p.poll() 
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break

def getDockerComposeFile(directory, specifications):
	specifications.insert(0, "docker-compose")
	specifications.append("yml")
	specificationString = reduce(lambda tot, spec: tot + "." + spec, specifications)
	return directory + "/" + specificationString

def getMainDockerComposeFile():
	return getDockerComposeFile(".", [])

def addDockerComposeFile(command, dockerComposeFile):
	command += " -f " + dockerComposeFile
	return command

def buildCommand(build, prod, user):
	command = "docker-compose"
	command += addDockerComposeFile("", getMainDockerComposeFile())

	if prod:
		raise(NotImplementedError("Production support is not yet implemented"))
	else:
		flavor = "dev"
	command = addDockerComposeFile(command, getDockerComposeFile(flavor, [flavor]))

	if user is not None:
		command = addDockerComposeFile(command, getDockerComposeFile(flavor, [flavor, user]))

	command += " up"

	if build:
		command += " --build"
	return command

@click.command()
@click.option("--build", is_flag=True, help="Build before running.")
@click.option("--prod", is_flag=True, help="Run/Build in production.")
@click.option("--user", help="The user to build/run for.")
def dc(build, prod, user):
	command = buildCommand(build, prod, user)
	print(command)
	for line in runCommand(command):
		click.echo(line)

if __name__ == '__main__':
	dc()