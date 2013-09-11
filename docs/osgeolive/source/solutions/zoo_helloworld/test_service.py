def Hello(conf, inputs, outputs):
    msg = "Hello {} from ZOO!".format(inputs['name']['value'])
    outputs['Result']['value'] = msg
    return 3  # SUCCEEDED
