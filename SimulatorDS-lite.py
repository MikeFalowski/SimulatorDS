#    "$Name:  $";
#    "$Header: /cvsroot/tango-ds/Simulators/SimulatorDS/SimulatorDS.py,v 1.4 2008/11/21 11:51:44 sergi_rubio Exp $";
#=============================================================================
#
# file :        SimulatorDS.py
#
# description : Python source for the SimulatorDS and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                SimulatorDS are implemented in this file.
#
# project :     TANGO Device Server
#
# $Author:  srubio@cells.es
#
# $Revision: 1.4 $
#
# $Log: SimulatorDS.py,v $
# Revision 1.4  2008/11/21 11:51:44  sergi_rubio
# Adapted_to_fandango.dynamic.DynamicDS_template
#
# Revision 1.3  2008/11/21 11:46:30  sergi_rubio
# *** empty log message ***
#
# Revision 1.2  2008/01/21 14:46:30  sergi_rubio
# Solved default properties initialization
#
# Revision 1.1.1.1  2007/10/17 16:44:12  sergi_rubio
# A Simulator for attributes and states, using dynamic attributes
#
# $Log:  $
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import sys
import traceback

import PyTango
import fandango
from fandango.dynamic import DynamicDS,DynamicDSClass,DynamicAttribute

#==================================================================
#   SimulatorDS Class Description:
#
#         <p>This device requires <a href="http://www.tango-controls.org/Documents/tools/fandango/fandango">Fandango module<a> to be available in the PYTHONPATH.</p>
#         <p>
#         This Python Device Server will allow to declare dynamic attributes which values will depend on a given time-dependent formula:
#         </p>
#         <h5 id="Example:">Example:</h5>
#         <pre class="wiki">  Square=0.5+square(t) #(t = seconds since the device started)
#         NoisySinus=2+1.5*sin(3*t)-0.5*random()
#         SomeNumbers=DevVarLongArray([1000.*i for i in range(1,10)])
#         </pre><p>
#         Attributes are DevDouble by default, but any Tango type or python expression can be used for declaration. <br>
#         Format is specified at <a class="ext-link" href="http://www.tango-controls.org/Members/srubio/dynamicattributes"><span class="icon">tango-controls.org</span></a>
#         </p>
#         <p>
#         Signals that can be easily generated with amplitude between 0.0 and 1.0 are:
#         </p>
#         <blockquote>
#         <p>
#         rampt(t), sin(t), cos(t), exp(t), triangle(t), square(t,duty), random()
#         </p>
#         </blockquote>
#         <p>
#         The MaxValue/MinValue property for each Attribute will determine the State of the Device only if the property DynamicStates is not defined.
#         </p>
#         <p>
#         If defined, <strong>DynamicStates</strong> will use this format:
#         </p>
#         <pre class="wiki">  FAULT=2*square(0.9,60)
#         ALARM=NoisySinus
#         ON=1
#         </pre><p>
#         This device inherits from <strong>fandango.dynamic.DynamicDS</strong> Class
#         </p>
#
#==================================================================


class SimulatorDS(DynamicDS): #PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
        #PyTango.Device_4Impl.__init__(self,cl,name)
        print 'IN SimulatorDS.__INIT__'
        
        ##Loading special methods to be available in formulas
        _locals = {}
        from re import match,search,findall
        _locals.update({'match':match,'search':search,'findall':findall})
        import re,math,random
        _locals.update((k,v) for m in (re,math,random) for k,v in  m.__dict__.items()  if not k.startswith('_'))
        try:
            import Signals
            _locals.update((k,v) for k,v in  Signals.__dict__.items() if not k.startswith('_'))
        except: print 'Unable to import custom Signals module'
        
        DynamicDS.__init__(self,cl,name,_locals=_locals,useDynStates=True)
        SimulatorDS.init_device(self)

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        print "[Device delete_device method] for device",self.get_name()


#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        print "In ", self.get_name(), "::init_device()"
        self.setLogLevel('DEBUG')
        self.set_state(PyTango.DevState.ON)
        #self.get_device_properties(self.get_device_class()) #Default values of properties already initialized by DynamicDS.__init__()
        #print 'SimulatorDS Property values are:\n'+'\n'.join('\t%s:\t%s'%(k,getattr(self,k)) for k in DynamicDSClass.device_property_list)
        self.get_DynDS_properties()
        if self.DynamicStates: self.set_state(PyTango.DevState.UNKNOWN)
        print "Out of ", self.get_name(), "::init_device()"

#------------------------------------------------------------------
#    Always excuted hook method
#------------------------------------------------------------------
    def always_executed_hook(self):
        print "In ", self.get_name(), "::always_excuted_hook()"
        DynamicDS.always_executed_hook(self)

#==================================================================
#
#    SimulatorDS read/write attribute methods
#
#==================================================================
#------------------------------------------------------------------
#    Read Attribute Hardware
#------------------------------------------------------------------
    def read_attr_hardware(self,data):
        print "In ", self.get_name(), "::read_attr_hardware()"


#==================================================================
#
#    SimulatorDS command methods
#
#==================================================================
    
#==================================================================
#
#    SimulatorDSClass class definition
#
#==================================================================
class SimulatorDSClass(DynamicDSClass):

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'DynamicAttributes':
            [PyTango.DevVarStringArray,
            "Attributes and formulas to create for this device.\n<br/>\nThis Tango Attributes will be generated dynamically using this syntax:\n<br/>\nT3=int(SomeCommand(7007)/10.)\n\n<br/>\nSee the class description to know how to make any method available in attributes declaration.",
            [ ] ],
        'DynamicStates':
            [PyTango.DevVarStringArray,
            "This property will allow to declare new States dinamically based on\n<br/>\ndynamic attributes changes. The function Attr will allow to use the\n<br/>\nvalue of attributes in formulas.<br/>\n\n\n<br/>\nALARM=Attr(T1)>70<br/>\nOK=1",
            [ ] ],
        }


    #    Command definitions
    cmd_list = {
        }


    #    Attribute definitions
    attr_list = {
        }


#------------------------------------------------------------------
#    SimulatorDSClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name);
        print "In SimulatorDSClass  constructor"

#==================================================================
#
#    SimulatorDS class main method
#
#==================================================================
if __name__ == '__main__':
    try:
        #py = PyTango.Util(sys.argv) #Rewritten because name of file doesnt match servers name
        py = PyTango.Util(['SimulatorDS',[a for a in sys.argv if not a.startswith('-')][-1]])
        py.add_TgClass(SimulatorDSClass,SimulatorDS,'SimulatorDS')
        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',traceback.format_exc()
    except Exception,e:
        print '-------> An unforeseen exception occured....',traceback.format_exc()
