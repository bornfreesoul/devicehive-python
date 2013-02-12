# -*- coding: utf-8 -*-
# vim:set et tabstop=4 shiftwidth=4 nu nowrap fileencoding=utf-8 encoding=utf-8:


from zope.interface import Interface, Attribute


class INotification(Interface):
    name = Attribute('Notification Name')
    parameters = Attribute('Dictionary of Notification Parameters')
    
    def to_dict(self):
        """
        @return dict representation of the object
        """


class ICommand(Interface):
    id = Attribute('Command identifier')
    timestamp = Attribute('Command timestamp (UTC)')
    user_id = Attribute('Associated user identifier')
    command = Attribute('Command name')
    parameters = Attribute('Command parameters, a dict object with an arbitrary structure')
    lifetime = Attribute('Command lifetime, a number of seconds until this command expires')
    flags = Attribute('Command flags, and optional value that could be supplied for device or related infrastructure')
    status = Attribute('Command status, as reported by device or related infrastructure')
    result = Attribute('Command execution result, and optional value that could be provided by device')
    
    def to_dict(self):
        """
        @return dict representation of the object
        """


class ICommandResult(Interface):
    status = Attribute('Status')
    result = Attribute('Command result. May be a string or an object.')
    def to_dict(self):
        """
        @return dict representation of the object
        """


class INetwork(Interface):
    id = Attribute('Network identifier')
    name = Attribute('Network Name')
    description = Attribute('Network Description')
    key = Attribute('Network Key')
    def to_dict(self):
        """
        @return dict representation of the object
        """


class IDeviceClass(Interface):
    name = Attribute('Device Class Name')
    version = Attribute('Device Class Version')
    is_permanent = Attribute('Whether Device Class is Permanent')
    def to_dict(self):
        """
        @return dict representation of the object
        """


class IEquipment(Interface):
    name = Attribute('Equipment display name')
    code = Attribute('Equipment code')
    typename = Attribute('Equipment type')
    data = Attribute('Equipment data, a dict object with an arbitrary structure')
    
    def to_dict(self):
        """
        @return dict representation of the object
        """


class IDeviceInfo(Interface):
    id = Attribute('Device ID')
    key = Attribute('Device Key')
    name = Attribute('Device Name')
    status = Attribute('Device Status')
    data = Attribute('Device data, a dict object with an arbitrary structure')
    network = Attribute('Network identifier or Network object which implements INetwork interface')
    device_class = Attribute('device class identifier or device class object which implements IDeviceClass interface')
    equipment = Attribute('List of IEquipment objects')
    
    def to_dict(self):
        """
        @return dict representation of the object
        """


class IProtoHandler(Interface):
    factory = Attribute('Reference to the owned factory/object which implements IProtoFactory')
    
    def on_failure(self, reason):
        """
        Called as a reaction on any unhandled error
        """
    
    def on_apimeta(self, websocket_server, server_time):
        """
        Reaction on ApiMeta call.
        
        @param websocket_server - url of devicehive websocket server
        @param server_time - current server time
        """
    
    def on_connected(self):
        """
        This callback is called upon connection has been established.
        """
    
    def on_closing_connection(self):
        """
        Called when server wants to close transport connection.
        """
    
    def on_command(self, device_id, command, finished):
        """
        Is called in reaction to command/insert received from devicehive server.
        
        @type device_id: C{str}
        @param device_id: device unique identifier.
        
        @type command: C{object}
        @param command: object which implements C{ICommand} interface.
        
        @return finished: A deferred object. When command finishes its execution user has to call this deferred's callback.
        """
    
    def on_failure(self, device_id, reason):
        """
        @type device_id: C{str}
        @param device_id: device guid. device_id may be None what means general system failure.
        """


class IProtoFactory(Interface):
    def authenticate(self, device_id, device_key):
        """
        Sends authentication message.
        
        @param device_id - device id
        @param device_key - device key
        @return deferred
        """
    
    def notify(self, notification, params, device_id = None, device_key = None):
        """
        Sends notification message to devicehive server.
        
        @param notification - notification identifier
        @param param - dictionary of notification parameters
        @return deferred
        """
    
    def update_command(self, command, device_id = None, device_key = None):
        """
        Updates an existing device command.
        
        @type command: C{obj}
        @param command: object which implements C{ICommand}
        
        @return deferred
        """
    
    def subscribe(self, device_id = None, device_key = None):
        """
        Subscribes a device to commands.
        
        @type device_id: C{str}
        @param device_id: device identifier (GUID)
        
        @type device_key: C{str}
        @param device_key: A device key. Optional parameter.
        
        @return deferred
        """ 
    
    def unsubscribe(self, device_id = None, device_key = None):
        """
        Unsubscribe a device from commands reception.
        
        @type device_id: C{str}
        @param device_id: device identifier (GUID)
        
        @type device_key: C{str}
        @param device_key: device name
        
        @return deferred
        """
    
    def device_save(self, info):
        """
        Registers or updates a device. A valid device key is required in the deviceKey parameter
        in order to update an existing device.
        
        @type info: C{object}
        @param info: object which implements C{IDeviceInfo} interface
        
        @return deferred
        """

