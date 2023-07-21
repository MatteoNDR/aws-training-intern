import http.client
import json

def lambda_handler(event, context):
    try:
        with open('endpoint.json', 'r') as file:
            data = json.load(file)

        response_data_list = []

        for endpoint_info in data:
            host = endpoint_info.get('host')
            port = endpoint_info.get('port')
            path = endpoint_info.get('path')

            try:
                connection = http.client.HTTPConnection(host, port, timeout=10)
                connection.request('GET', path)
                response = connection.getresponse()
                print("Status: {} - reason: {}".format(response.status, response.reason))

                response_body = response.read().decode()
                if response_body:
                    response_data = json.loads(response_body)
                    print("Response Data:", response_data)

                    errore_value = response_data.get("errore")
                    if errore_value is None:
                        print("Nessun errore trovato")
                    else:
                        print("Errore trovato:", errore_value)
                else:
                    response_data = None

            except Exception as e:
                print(f"Errore nell'endpoint {host}:{port}{path}: {str(e)}")
                response_data = None

            finally:
                connection.close()

            response_data_list.append(response_data)

        return {
            'statusCode': 200,
            'body': response_data_list
        }

    except Exception as e:
        request_body = json.dumps(event)
        print("Request Body:", request_body)
        return {
            'statusCode': 500,
            'body': f'Db down con errore: {str(e)}'
        }