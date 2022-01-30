"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""
import os
import pandas as pd
from collections import defaultdict
from datetime import datetime
from flask import request, send_file
from flask_restplus import Resource

from .security import require_auth
from . import api_rest


wav_source_path = "/home/samba/public/Results/Test/resource/wav"

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@api_rest.route('/wav/id')
class ResourceID(Resource):
    def get(self):
        type_list = os.listdir(wav_source_path)
        resource_id_list = []
        for type in type_list:
            resource_id_list.extend(os.listdir(os.path.join(wav_source_path, type)))
        resource_id_list = sorted(list(set(resource_id_list)))
        return {'resource_id_list': resource_id_list}

@api_rest.route('/wav/type/<string:resource_id>')
class WavResourceType(Resource):
    """
    WavResourceType 
    """
    def get(self, resource_id):
        """
        Returns a list of types for a given resource_id
        """
        resource_type = []
        type_list = os.listdir(wav_source_path)
        for item in type_list:
            if resource_id in os.listdir(os.path.join(wav_source_path, item)):
                resource_type.append(item)

        return {"resource_type": resource_type}


@api_rest.route('/wav/path/<string:type>/<string:resource_id>')
class WavPathResource(Resource):
    """
    WavPathResource
    """
    def get(self, type, resource_id):
        """
        Get wav path
        """
        wav_dir = os.path.abspath(os.path.join(wav_source_path, type, resource_id))
        model_list = []
        wav_list = []
        text_list = []
        for model in os.listdir(wav_dir):
            if os.path.isdir(os.path.join(wav_dir, model)):
                model_list.append(model)
        with open(os.path.join(wav_dir, "test.txt"), "r") as f:
            for line in f.readlines():
                wav_list.append(line.strip().split("|")[0] + ".wav")
                text_list.append(line.strip().split("|")[1])
                   
        return {"model_list": model_list, "wav_list": wav_list, "text_list": text_list}

    def post(self, type, resource_id):
        """
        Post wav path
        """
        json_payload = request.json
        model_list = json_payload["model_list"]
        wav_list = json_payload["wav_list"]
        model_wav_score_list = json_payload["model_wav_score_list"]

        result_path = os.path.abspath(os.path.join(wav_source_path, type, resource_id, f"{type}_result.csv"))
        df_columns = ["time", "user", "id", "type", "model", "wav", "score"]
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if os.path.exists(result_path):
            result = pd.read_csv(result_path)
        else:
            open(result_path, "w").close()
            result = pd.DataFrame(columns=df_columns)

        user = result.user.max() + 1 if len(result) > 0 else 1        

        for model in model_list:
            for wav_index in range(len(wav_list)):
                wav = wav_list[wav_index]
                score = model_wav_score_list[model][wav_index]
                result = result.append({"time": now_time, "user": user, "id": resource_id, "type": type, "model": model, "wav": wav, "score": score}, ignore_index=True)
        result.to_csv(result_path, index=False)

        return {"status": "ok"}

@api_rest.route('/wav/result/<string:type>/<string:resource_id>')
class WavResultResource(Resource):
    """
    WavResultResource
    """
    def get(self, type, resource_id):
        """
        Get wav result
        """
        result_path = os.path.abspath(os.path.join(wav_source_path, type, resource_id, f"{type}_result.csv"))
        df_columns = ["time", "user", "id", "type", "model", "wav", "score"]

        if os.path.exists(result_path):
            result = pd.read_csv(result_path)
        else:
            return {"status": "no result"}
        model_wav_result = result.groupby(["model", "wav"]).mean()
        model_result = result.groupby(["model"]).mean()
        model_list, wav_list = result["model"].unique().tolist(), result["wav"].unique().tolist()
        model_wav_score_list = defaultdict(dict)
        model_score_list = defaultdict(dict)
        for model in model_list:
            for wav in wav_list:
                model_wav_score_list[model][wav] = model_wav_result["score"].loc[model, wav].item()
            model_score_list[model] = model_result["score"].loc[model].item()

            
        return {"model_wav_score_list": dict(model_wav_score_list), "model_score_list": dict(model_score_list)}

# @api_rest.route('/wav/resource/<wav_path>')
# class WaveResource(Resource):
#     """
#     WaveResource
#     """
#     def get(self, wav_path):
#         """
#         Get wav resource

#         """
#         wav_path = os.path.abspath(os.path.join(wav_source_path, wav_path))
#         print(wav_path)
#         if os.path.exists(wav_path):
#             return send_file(wav_path, mimetype='audio/wav', as_attachment=True)
#         else:
#             return {"error": "wav file not found"}

@api_rest.route('/wav/resource/<string:type>/<string:resource_id>/<string:model>/<string:wav_name>')
class WaveResource(Resource):
    """
    WaveResource
    """
    def get(self, type, resource_id, model, wav_name):
        """
        Get wav resource

        """
        wav_path = os.path.abspath(os.path.join(wav_source_path, type, resource_id, model, wav_name))
        if os.path.exists(wav_path):
            return send_file(wav_path, mimetype='audio/wav', as_attachment=True)
        else:
            return {"error": "wav file not found"}

@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
