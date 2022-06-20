# -*- coding: utf-8 -*-
import time
from urllib import request

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models

from config import Config

class TencentSDK(object):
    def __init__(self, secret_id, secret_key) -> None:
        cred = credential.Credential(secret_id, secret_key)
        self.client = tts_client.TtsClient(cred, "ap-shanghai")

        self.text = ''
        self.voice_type = 100510000
        self.sample_rate = 16000
        self.codec = 'mp3'
        self.speed = 0
        self.volume = 0
        self.voiceover_dialogue_split = True

        self.model_type = 1
        self.project_id = 0
        self.primary_language = 1

    def create_task(self) -> str:
        task_id = ''

        req = models.CreateTtsTaskRequest()
        req.Text = self.text
        req.VoiceType = self.voice_type
        req.VoiceoverDialogueSplit = self.voiceover_dialogue_split
        req.Codec = self.codec
        req.SampleRate = self.sample_rate
        req.ModelType = self.model_type
        try:
            resp = self.client.CreateTtsTask(req)
            task_id = resp.Data.TaskId
            req_id = resp.RequestId
            print('call CreateTtsTask succeed, task_id: {} request_id: {}'.format(task_id, req_id))
        except TencentCloudSDKException as err:
            print('call CreateTtsTask failed, err: {}'.format(str(err)))
        
        return task_id

    def query_task(self, task_id):
        req = models.DescribeTtsTaskStatusRequest()
        req.TaskId = task_id
        try:
            resp = self.client.DescribeTtsTaskStatus(req)
            data = resp.Data
            req_id = resp.RequestId
            print('call DescribeTtsTaskStatus succeed, data: {} request_id: {}'.format(str(data), req_id))
        except TencentCloudSDKException as err:
            print('call DescribeTtsTaskStatus failed, err: {}'.format(str(err)))

        if data:
            return data.Status, data.ErrorMsg, data.ResultUrl
        else:
            return 3, 'internal error', ''

    def long_text_synthesis(self, text):
        audio_url = ''

        self.text = text
        task_id = self.create_task()
        if not task_id:
            return audio_url

        while True:
            status, msg, audio_url = self.query_task(task_id)
            if status in (0, 1):
                time.sleep(10) # sleep 10 seconds
                continue
            if status == 3:
                print('synthesis failed, error msg: {}'.format(msg))
                break
            if status == 2:
                print('synthesis succeed, audio url: {}'.format(audio_url))
                break
        
        return audio_url


def main():
    text = '夜云英俊的面庞突然激动起来，他紧紧握住自己的双拳，恨恨的说道：“不，我一定不会让他们得逞的，死也不会。这里是我们的家园，没有谁能赶我们走。”由于握的过紧，他手上的骨骼咯咯做响，在寂静的夜晚中听起来带着一丝诡异。'
    cloud = TencentSDK(Config.SECRET_ID, Config.SECRET_KEY)
    audio_url = cloud.long_text_synthesis(text)
    print('合成文本: "{}"'.format(text))
    if audio_url:
        print('合成音频: {}'.format(audio_url))
    else:
        print('合成失败')

if __name__ == '__main__':
    main()
