"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""
import os
import shutil
import pandas as pd
from collections import defaultdict
from datetime import datetime
from flask import request, send_file
from flask_restplus import Resource

from .security import require_auth
from . import api_rest


wav_source_path = "/home/samba/public/Results/Test/resource/wav"
video_source_path = "/home/samba/public/Results/Test/resource/video"
wav_api_prefix= '/api/wav/resource'
video_api_prefix= '/api/video/resource'

"""
API for WAV
"""
class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@api_rest.route('/wav/id')
class ResourceID(Resource):
    def get(self):
        type_list = os.listdir(wav_source_path)
        resource_id_list = []
        for type in type_list:
            resource_id_list.extend(os.listdir(
                os.path.join(wav_source_path, type)))
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
        front_model_name = ['reconstruct', 'raw']
        model_wav_score_list = defaultdict(dict)
        model_wav_list = defaultdict(dict)
        for model in os.listdir(wav_dir):
            if os.path.isdir(os.path.join(wav_dir, model)):
                model_list.append(model)
        for name in front_model_name:
            if name in model_list:
                model_list.remove(name)
                model_list.insert(0, name)
        with open(os.path.join(wav_dir, "test.txt"), "r") as f:
            for line in f.readlines():
                wav_list.append(line.strip().split("|")[0] + ".wav")
                text_list.append(line.strip().split("|")[1])
        for model in model_list:
            for wav in wav_list:
                model_wav_list[model][wav] = '/'.join([wav_api_prefix, type, resource_id, model, wav]) # wav_path ?????????
                model_wav_score_list[model][wav] = 3.0 # ???????????????
                   
        return {
            "model_list": model_list,
            "wav_list": wav_list, 
            "text_list": text_list, 
            "model_wav_list": dict(model_wav_list),
            "model_wav_score_list": dict(model_wav_score_list)
        }

    def post(self, type, resource_id):
        """
        Post wav path
        """
        json_payload = request.json
        model_list = json_payload["model_list"]
        wav_list = json_payload["wav_list"]
        model_wav_score_list = json_payload["model_wav_score_list"]

        df_columns = ["time", "user", "id", "type", "model", "wav", "score"]
        now_time = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")

        result_path = os.path.abspath(os.path.join(wav_source_path, type, resource_id, f"result.csv"))
        new_path = os.path.abspath(os.path.join(wav_source_path, type, resource_id, f"{now_time}.csv"))

        if os.path.exists(result_path):
            result = pd.read_csv(result_path)
        else:
            result = pd.DataFrame(columns=df_columns)
            result.to_csv(result_path, index=False)
        new_data = pd.DataFrame(columns=df_columns)
        new_data.to_csv(new_path, index=False)

        user = result.user.max() + 1 if len(result) > 0 else 1   
        
        for model in model_list:
            for wav_index in range(len(wav_list)):
                wav = wav_list[wav_index]
                score = model_wav_score_list[model][wav]
                data_dict = {"time": now_time, "user": user, "id": resource_id,
                             "type": type, "model": model, "wav": wav, "score": score}
                result = result.append(data_dict, ignore_index=True)
                new_data = new_data.append(data_dict, ignore_index=True)
        result.to_csv(result_path, index=False)
        new_data.to_csv(new_path, index=False)
        print(result)

        return {"message": "ok"}

    def delete(self, type, resource_id):
        """
        Delete wav path
        """
        result_path = os.path.abspath(os.path.join(
            wav_source_path, type, resource_id, f"result.csv"))
        if os.path.exists(result_path):
            os.remove(result_path)
        return {"message": "ok"}

@api_rest.route('/wav/result/<string:type>/<string:resource_id>')
class WavResultResource(Resource):
    """
    WavResultResource
    """
    def get(self, type, resource_id):
        """
        Get wav result
        """
        result_path = os.path.abspath(os.path.join(wav_source_path, type, resource_id, f"result.csv"))
        df_columns = ["time", "user", "id", "type", "model", "wav", "score"]

        if os.path.exists(result_path):
            result = pd.read_csv(result_path)
        else:
            return {"message": "no result"}
        model_wav_result = result.groupby(["model", "wav"]).mean()
        model_result = result.groupby(["model"]).mean()
        model_list, wav_list = result["model"].unique().tolist(), result["wav"].unique().tolist()
        model_wav_score_list = defaultdict(dict)
        model_score_list = defaultdict(dict)
        for model in model_list:
            for wav in wav_list:
                model_wav_score_list[model][wav] = model_wav_result["score"].loc[model, wav].item()
            model_score_list[model] = model_result["score"].loc[model].item()

            
        return {
            "model_list": model_list,
            "wav_list": wav_list,
            "model_wav_score_list": dict(model_wav_score_list),
            "model_score_list": dict(model_score_list)
        }

# @api_rest.route('/wav/resource/<string:wav_path>')
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


"""
API for VIDEO
"""

@api_rest.route('/video/id')
class ResourceID(Resource):
    def get(self):
        type_list = os.listdir(video_source_path)
        resource_id_list = []
        for type in type_list:
            resource_id_list.extend(os.listdir(
                os.path.join(video_source_path, type)))
        resource_id_list = sorted(list(set(resource_id_list)))
        return {'resource_id_list': resource_id_list}


@api_rest.route('/video/type/<string:resource_id>')
class VideoResourceType(Resource):
    """
    VideoResourceType 
    """

    def get(self, resource_id):
        """
        Returns a list of types for a given resource_id
        """
        resource_type = []
        type_list = os.listdir(video_source_path)
        for item in type_list:
            if resource_id in os.listdir(os.path.join(video_source_path, item)):
                resource_type.append(item)

        return {"resource_type": resource_type}


@api_rest.route('/video/path/<string:type>/<string:resource_id>')
class VideoPathResource(Resource):
    """
    VideoPathResource
    """

    def get(self, type, resource_id):
        """
        Get video path
        """
        video_dir = os.path.abspath(os.path.join(
            video_source_path, type, resource_id))
        print(video_dir)
        model_list = []
        video_list = []
        text_list = []
        front_model_name = ['reconstruct', 'raw']
        model_video_score_list = defaultdict(dict)
        model_video_list = defaultdict(dict)
        for model in os.listdir(video_dir):
            if os.path.isdir(os.path.join(video_dir, model)):
                model_list.append(model)
        for name in front_model_name:
            if name in model_list:
                model_list.remove(name)
                model_list.insert(0, name)
        with open(os.path.join(video_dir, "test.txt"), "r") as f:
            for line in f.readlines():
                video_list.append(line.strip().split("|")[0] + ".mp4")
                text_list.append(line.strip().split("|")[1])
        for model in model_list:
            for video in video_list:
                # video_path ?????????
                model_video_list[model][video] = '/'.join(
                    [video_api_prefix, type, resource_id, model, video])
                model_video_score_list[model][video] = 3.0  # ???????????????

        return {
            "model_list": model_list,
            "video_list": video_list,
            "text_list": text_list,
            "model_video_list": dict(model_video_list),
            "model_video_score_list": dict(model_video_score_list)
        }

    def post(self, type, resource_id):
        """
        Post video path
        """
        json_payload = request.json
        model_list = json_payload["model_list"]
        video_list = json_payload["video_list"]
        model_video_score_list = json_payload["model_video_score_list"]

        df_columns = ["time", "user", "id", "type", "model", "video", "score"]
        now_time = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")

        result_path = os.path.abspath(os.path.join(
            video_source_path, type, resource_id, f"result.csv"))
        new_path = os.path.abspath(os.path.join(
            video_source_path, type, resource_id, f"{now_time}.csv"))

        if os.path.exists(result_path):
            result = pd.read_csv(result_path)
        else:
            result = pd.DataFrame(columns=df_columns)
            result.to_csv(result_path, index=False)
        new_data = pd.DataFrame(columns=df_columns)
        new_data.to_csv(new_path, index=False)

        user = result.user.max() + 1 if len(result) > 0 else 1

        for model in model_list:
            for video_index in range(len(video_list)):
                video = video_list[video_index]
                score = model_video_score_list[model][video]
                data_dict = {"time": now_time, "user": user, "id": resource_id,
                             "type": type, "model": model, "video": video, "score": score}
                result = result.append(data_dict, ignore_index=True)
                new_data = new_data.append(data_dict, ignore_index=True)
        result.to_csv(result_path, index=False)
        new_data.to_csv(new_path, index=False)
        print(result)

        return {"message": "ok"}

    def delete(self, type, resource_id):
        """
        Delete video path
        """
        result_path = os.path.abspath(os.path.join(
            video_source_path, type, resource_id, f"result.csv"))
        if os.path.exists(result_path):
            os.remove(result_path)
        return {"message": "ok"}


@api_rest.route('/video/resource/<string:type>/<string:resource_id>/<string:model>/<string:video_name>')
class VideoResource(Resource):
    """
    VideoResource
    """

    def get(self, type, resource_id, model, video_name):
        """
        Get wav resource

        """
        video_path = os.path.abspath(os.path.join(
            video_source_path, type, resource_id, model, video_name))
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4', as_attachment=True)
        else:
            return {"error": "video file not found"}

# @api_rest.route('/video/result/<string:type>/<string:resource_id>')
# class VideoResultResource(Resource):
#     """
#     VideoResultResource
#     """

#     def get(self, type, resource_id):
#         """
#         Get Video result
#         """
#         result_path = os.path.abspath(os.path.join(
#             video_source_path, type, resource_id, f"result.csv"))
#         df_columns = ["time", "user", "id", "type", "model", "wav", "score"]

#         if os.path.exists(result_path):
#             result = pd.read_csv(result_path)
#         else:
#             return {"message": "no result"}
#         model_wav_result = result.groupby(["model", "wav"]).mean()
#         model_result = result.groupby(["model"]).mean()
#         model_list, wav_list = result["model"].unique(
#         ).tolist(), result["wav"].unique().tolist()
#         model_wav_score_list = defaultdict(dict)
#         model_score_list = defaultdict(dict)
#         for model in model_list:
#             for wav in wav_list:
#                 model_wav_score_list[model][wav] = model_wav_result["score"].loc[model, wav].item(
#                 )
#             model_score_list[model] = model_result["score"].loc[model].item()

#         return {
#             "model_list": model_list,
#             "wav_list": wav_list,
#             "model_wav_score_list": dict(model_wav_score_list),
#             "model_score_list": dict(model_score_list)
#         }



"""
DEMO
"""
# @api_rest.route('/resource/<string:resource_id>')
# class ResourceOne(Resource):
#     """ Unsecure Resource Class: Inherit from Resource """

#     def get(self, resource_id):
#         timestamp = datetime.utcnow().isoformat()
#         return {'timestamp': timestamp}

#     def post(self, resource_id):
#         json_payload = request.json
#         return {'timestamp': json_payload}, 201


# @api_rest.route('/secure-resource/<string:resource_id>')
# class SecureResourceOne(SecureResource):
#     """ Unsecure Resource Class: Inherit from Resource """

#     def get(self, resource_id):
#         timestamp = datetime.utcnow().isoformat()
#         return {'timestamp': timestamp}
