# ========================================================================
#  Licensed Materials - Property of IBM
#  "Restricted Materials of IBM"
#
#  IBM SDK, Java(tm) Technology Edition, v8
#  (C) Copyright IBM Corp. 2000, 2014. All Rights Reserved
#
#  US Government Users Restricted Rights - Use, duplication or disclosure
#  restricted by GSA ADP Schedule Contract with IBM Corp.
# ========================================================================
                    NetBeans Project Files for JDK Demos
This directory contains project files for the NetBeans IDE for the all-Java
JDK demos (some of the demos involve C code; no NetBeans project files are
provided for them at this time).  For example, to bring up the Java2D demo
in NetBeans, do the following:

1. If you do not already have NetBeans, download it from
     http://www.netbeans.org/
   and follow the directions for installation.
2. Start NetBeans.
3. From the main menu, choose File -> Open Project.
4. In the popup window, navigate to the JDK distribution and within that to
   the "demo" directory.
5. Press the "Open Project Folder" button.  That will open all of the demos
   (for which there are project files) as subprojects.
6. There should now be a Java2D project in the Projects tab of the IDE.
   Right-click on the project name and choose an appropriate action, e.g.
     Clean and Build Project
   and then
     Run Project
   Some, but not all, of the projects can be run as applets as well.

Documentation and support for NetBeans is available at the NetBeans web site:
     http://www.netbeans.org/

Notes:
 1. jconsole-plugin is a special kind of project, a plugin for jconsole.
    Therefore it is not possible to run the project directly from the IDE.
