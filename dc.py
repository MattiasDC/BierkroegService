import click
import subprocess

def runCommand(command):    
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
        # returns None while subprocess is running
        retcode = p.poll() 
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break

@click.command()
@click.option("--build", is_flag=True, help="Build before running.")
@click.option("--prod", is_flag=True, help="Run/Build in production.")
@click.option("--user", help="The user to build/run for.")
def dc(build, prod, user):
	dcString = "docker-compose"
	extension = ".yml"
	
	command = ""
	if build:
		command += "sudo "
	command += dcString + " -f " + dcString + extension

	if prod:
		flavor = "prod"
	else:
		flavor = "dev"
	command += " -f " + flavor + "/" + dcString + "." + flavor + extension

	if user is not None: 
		command += " -f " + flavor + "/" + dcString + "." + flavor + "." + user + extension

	command += " up"

	if build:
		command += " --build"
	
	for line in runCommand(command):
		click.echo(line)

if __name__ == '__main__':
    dc()