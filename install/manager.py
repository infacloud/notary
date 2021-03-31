import ruamel.yaml
import argparse
import json

class NotaryManager:

    NOTARY_JSON = "notary_env.json"
    CONFIG_JSON = "data/config/server-config.json"

    def get_data(self, account, environment):
        try:
            notary_json_file = open(NotaryManager.NOTARY_JSON)
            notary_json = json.load(notary_json_file)
            notary_json_file.close()
            return notary_json[account][environment]
        except Exception as ex:
            return None

    def prepare_notary_build(self, account, environment):
        notary_json = self.get_data(account, environment)
        self.modify_notary_yaml(notary_json)
        self.modify_notary_config(notary_json)

    def modify_notary_config(self, notary_json):
        try:
            hostname = notary_json['host']
            with open(NotaryManager.CONFIG_JSON) as fp:
                data =json.load(fp)
            fp.close()
            data['trust_service']['hostname'] = hostname
            with open(NotaryManager.CONFIG_JSON,'w') as fp:
                json.dump(data, fp, indent=2)
            fp.close()
        except Exception as ex:
            print("ERROR: While modifying notary config file : "+str(ex))

    def modify_notary_yaml(self, notary_json):
        if notary_json:
            try:
                file = "../template-ct-docker-compose.yml"
                with open(file) as fp:
                    data = ruamel.yaml.load(fp,  ruamel.yaml.RoundTripLoader)
                fp.close()
                data['services']['server']['image'] = notary_json['server_image']
                data['services']['signer']['image'] = notary_json['signer_image']
                data['services']['mysql']['image'] = notary_json['db_image']
                data['services']['signer']['networks']['sig']['aliases'][0] = notary_json['host']
                with open('../ct-docker-compose.yml','w') as fp:
                    ruamel.yaml.dump(data, fp, Dumper=ruamel.yaml.RoundTripDumper)
                fp.close()
            except Exception as ex:
                print("Error occured while reading the notary_env.json : Missing keys : "+str(ex))
        else:
            print("ERROR: Unable to parse the notary_env.json file!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Notary manager script.')
    parser.add_argument('-a','--action', type=str, required=True, choices=['build_commerical', 'build_fedramp'], help="Action needed for script to invoke build stages.")
    parser.add_argument('-env', '--environment', type=str, required=True, choices=['staging', 'prod'], help="Environment to build notary yaml.")
    params = parser.parse_args()
    action = params.action
    environment = params.environment
    print("Invoking manager script with action: {},  environment: {}".format(action, environment))
    if action.lower() == "build_commerical":
        nm = NotaryManager()
        nm.prepare_notary_build("commercial", environment)
    elif action.lower() == "build_fedramp":
        nm = NotaryManager()
        nm.prepare_notary_build("fedramp", environment)
    else:
        parser.print_help()
