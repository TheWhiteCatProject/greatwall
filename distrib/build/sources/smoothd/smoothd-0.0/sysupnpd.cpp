/* SysUpnpd Module for the SmoothWall SUIDaemon                           */
/* Contains functions relating to starting/restarting upnpd                  */
/* (c) 2007 SmoothWall Ltd                                                */
/* ----------------------------------------------------------------------  */
/* Original Author  : Lawrence Manning                                     */
/* Translated to C++: M. W. Houston                                        */

/* include the usual headers.  iostream gives access to stderr (cerr)     */
/* module.h includes vectors and strings which are important              */
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <syslog.h>
#include <signal.h>

#include "module.h"
#include "ipbatch.h"
#include "setuid.h"

extern "C" {
	int load(std::vector<CommandFunctionPair> &  );
	int restart_upnpd(std::vector<std::string> & parameters, std::string & response );
	int start_upnpd(std::vector<std::string> & parameters, std::string & response );
	int stop_upnpd(std::vector<std::string> & parameters, std::string & response );
}

int load(std::vector<CommandFunctionPair> & pairs )
{
	/* CommandFunctionPair name("command", "function" ); */
	CommandFunctionPair restart_upnpd_function("upnpdrestart", "restart_upnpd", 0, 0);
	CommandFunctionPair start_upnpd_function("upnpdstart", "start_upnpd", 0, 0);
	CommandFunctionPair stop_upnpd_function("upnpdstop", "stop_upnpd", 0, 0);

	pairs.push_back(restart_upnpd_function);
	pairs.push_back(start_upnpd_function);
	pairs.push_back(stop_upnpd_function);

	return 0;
}

int restart_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	
	error += stop_upnpd(parameters, response);
	
	if (!error)
		error += start_upnpd(parameters, response);
	
	if (!error)
		response = "Upnpd Restart Successful";
	
	return error;
}

int stop_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	
	killprocess("/var/run/miniupnpd.pid");

	response = "Miniupnpd process terminated";

	return error;
}

int start_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	ConfigSTR iface("/var/smoothwall/red/iface");
	ConfigSTR uuid("/etc/miniupnpd.uuid");
	std::vector<std::string> args;
	ConfigVAR settings("/var/smoothwall/advnet/settings");
	ConfigVAR netsettings("/var/smoothwall/ethernet/settings");

	args.push_back("/usr/sbin/miniupnpd");
	args.push_back("-f");
	args.push_back("/etc/miniupnpd.conf");
	args.push_back("-i");
	args.push_back(iface.str());
	args.push_back("-u");
	args.push_back(uuid.str());
	args.push_back("-U");
	
	if (netsettings["GREEN_DEV"] != "")
	{
		args.push_back("-a");
		args.push_back(netsettings["GREEN_ADDRESS"]);
	}
	if (netsettings["PURPLE_DEV"] != "")
	{
		args.push_back("-a");
		args.push_back(netsettings["PURPLE_ADDRESS"]);
	}
	
	/* Not an error really. */
	if (iface.str() == "")
		goto EXIT;

	if (settings["ENABLE_UPNP"] == "on")
	{
		error = simplesecuresystemvector(args);
		if (error)
			response = "Can't start minipnpd";
		else
			response = "Miniupnpd start successful";
	}
	
EXIT:
	return error;
}
