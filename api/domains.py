from flask import abort, make_response
import dns.resolver

# Data to serve with our API
custom_domains = {
    1: {
        'domain': 'custom.fi.uba.ar',
        'ip': '1.1.1.1'
    },
}

rr_dict = {}

# Create a handler for our read (GET) domains
def get(q=""):
    """
    Esta funcion maneja el request GET /api/custom-domains/?q={query}

     :q path:  palabra clave a buscar en los dominios
    :return:        200 dominios que cumplan con la query, 404 dominio no encontrado
    """
    # Create the list of domains from our data
    domains = {}
    domains["items"] = []
    if q != "":
        for domain in custom_domains.values():
            if q in domain["domain"]:
                domain["custom"] = True
                domains["items"].append(domain)
    else:
        for domain in custom_domains.values():
            domain["custom"] = True
            domains["items"].append(domain)
    return make_response(domains, 200)


def get_one(domain_name):
    """
    Esta funcion maneja el request GET /api/domain/{domain_name}

     :domain_name path:  nombre del dominio a obtener
    :return:        200 dominio, 404 dominio no encontrado
    """
    domains = []
    for domain in custom_domains.values():
        if domain['domain'] == domain_name:
            domains.append({"ip" :domain['ip'],"custom" : True})
    try:
        result = dns.resolver.query(domain_name)
        for ip in result:
            domains.append({"ip" :ip.address,"custom" : False})
    except:
        pass
    if domain_name not in rr_dict.keys() and len(domains) != 0:
        returned_ip = domains[0]
        rr_dict[domain_name] = returned_ip
        returned_ip['domain'] = domain_name
        return make_response(returned_ip, 200)
    elif len(domains) == 0:
        return abort(404, 'El dominio no fue encontrado')
    else:
        return_next = False
        for ip_dict in domains:
            if rr_dict[domain_name]['ip'] == ip_dict['ip'] \
                and  rr_dict[domain_name]["custom"] == ip_dict["custom"]:
                return_next = True
            elif return_next:
                rr_dict[domain_name] = ip_dict
                ip_dict['domain'] = domain_name
                return make_response(ip_dict, 200)
        returned_ip = domains[0]
        rr_dict[domain_name] = returned_ip
        returned_ip['domain'] = domain_name
        return make_response(returned_ip, 200)


def create(**kwargs):
    """
    Esta funcion maneja el request POST /api/custom-domains/

     :param body:  dominio a crear en la lista de custom-domains
    :return:        201 dominio creado, 400 dominio duplicado
    """
    dominio = kwargs.get('body')
    ip = dominio.get('ip')
    domain_name = dominio.get('domain')
    if not domain_name or not ip:
        return abort(400, 'custom domain already exists')

    dup = False
    for domain in custom_domains.values():
        dup = domain_name == domain.get('domain')
        if dup: break

    if dup:
        return abort(400, 'custom domain already exists')

    new_id = max(custom_domains.keys()) + 1
    custom_domains[new_id] = dominio.copy()
    custom_domains[new_id]['custom'] = True
    return make_response(dominio, 201)

def delete(domain_name):
    """
    Esta funcion maneja el request DELETE /api/custom-domains/{domain_name}

     :domain_name path:  nombre del dominio que se quiere borrar
    :return:        200 dominio borrado, 404 dominio no encontrado
    """
    exists = False
    for key, domain in custom_domains.items():
        exists = domain_name == domain.get('domain')
        id = key
        if exists: break
    if not exists:
        return abort(404, 'domain not found')

    del custom_domains[id]
    return make_response({'domain' : domain_name}, 200)

def edit(domain_name, **kwargs):
    """
    Esta funcion maneja el request PUT /api/custom-domains/{domain_name}

    :domain_name path:  nombre del dominio que se quiere editar
    :param body:  id del dominio que se quiere modificar
    :return:        200 dominio modificado, 404 dominio no encontrado
    """
    dominio = kwargs.get('body')
    body_domain_name = dominio.get('domain')
    ip = dominio.get('ip')

    if not domain_name or not ip or domain_name != body_domain_name:
        return abort(400, 'payload is invalid')

    exists = False
    for key, domain in custom_domains.items():
        exists = domain_name == domain.get('domain')
        id = key
        if exists: break
    if not exists:
        return abort(404, 'domain not found')

    custom_domains[id]['ip'] = ip
    return make_response({'domain':dominio['domain'],'ip':dominio['ip'],'custom':True}, 200)
