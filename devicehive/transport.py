def init(name, data_format, data_format_options, handler, handler_options):
    transport_class_name = '%sTransport' % name.title()
    transport_module = __import__('devicehive.transports.%s_transport' % name,
                                  fromlist=[transport_class_name])
    return getattr(transport_module, transport_class_name)(data_format,
                                                           data_format_options,
                                                           handler,
                                                           handler_options)
