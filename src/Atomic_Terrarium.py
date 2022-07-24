import json

def form_data(times,sensor, pub_topic):
                list = [times,str(sensor)]
                data = json.dumps(list)
                print("Publish to Topic" + pub_topic)
                print (str(sensor))
                return data


def aciona_irrigacao(data):
                if data == "AAA" :
                        return True
                else:
                        return False


                

