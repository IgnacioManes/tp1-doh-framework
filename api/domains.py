from flask import abort, make_response
import dns.resolver

# Data to serve with our API
custom_domains = {
    1: {
        'domain': 'custom.fi.una.ar',
        'ip': '1.1.1.1'
    },
}

# Create a handler for our read (GET) people
def get(q):
    """
    Esta funcion maneja el request GET /api/custom-domains/?q={query}

    :id_alumno body:  id del alumno que se quiere borrar
    :return:        200 alumno, 404 alumno no encontrado
    """
    # Create the list of people from our data
    return domains

def get_one(domain_name):
    """
    Esta funcion maneja el request GET /api/domain/{domain_name}

     :domain_name body:  nombre del dominio a obtener
    :return:        200 dominio, 404 dominio no encontrado
    """
    domains = []
    for domain in custom_domains:
        if domain['domain'] == domain_name:
            domains.append(domain)
    result = dns.resolver.query('www.yahoo.com')
    domains += result
    if domain_name not in domains:
        return abort(404, 'El dominio no fue encontrado')

    return alumnos.get(id_alumno)

def create(**kwargs):
    """
    Esta funcion maneja el request POST /api/alumnos

     :param body:  alumno a crear en la lista de alumnos
    :return:        201 alumno creado, 400 dni o padron duplicado
    """
    alumno = kwargs.get('body')
    dni = alumno.get('dni')
    padron = alumno.get('padron')
    nombre = alumno.get('nombre')
    if not dni or not padron or not nombre:
        return abort(400, 'Faltan datos para crear un alumno')

    dup = False
    for alumno_existente in alumnos.values():
        dup = dni == alumno_existente.get('dni') or padron == alumno_existente.get('padron')
        if dup: break

    if dup:
        return abort(400, 'DNI o Padron ya existentes')

    new_id = max(alumnos.keys()) + 1
    alumno['id'] = new_id
    alumnos[new_id] = alumno

    return make_response(alumno, 201)

def delete(id_alumno):
    """
    Esta funcion maneja el request DELETE /api/alumnos/{id_alumno}

    :id_alumno body:  id del alumno que se quiere borrar
    :return:        200 alumno, 404 alumno no encontrado
    """
    if id_alumno not in alumnos:
        return abort(404, 'El alumno no fue encontrado')

    del alumnos[id_alumno]

    return make_response('', 204)

def edit(id_alumno):
    """
    Esta funcion maneja el request DELETE /api/alumnos/{id_alumno}

    :id_alumno body:  id del alumno que se quiere borrar
    :return:        200 alumno, 404 alumno no encontrado
    """
    if id_alumno not in alumnos:
        return abort(404, 'El alumno no fue encontrado')

    del alumnos[id_alumno]

    return make_response('', 204)
