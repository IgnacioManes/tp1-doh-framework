import dns.resolver

# Resolve www.yahoo.com
result = dns.resolver.query('www.yahoo.com')
ips = [{"ip" : ip.address ,"custom" : False} for ip in result]
print(ips)
