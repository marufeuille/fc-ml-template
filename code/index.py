# -*- coding: utf-8 -*-
import logging
import json
import time

# 自分の環境に合わせて変えてください
import numpy as np
import sklearn
import pandas as pd
import tensorflow as tf
import pickle

from aliyun.log import *

from helper import MAE

# Initializerはコンテナ作成時に1度だけ実行されます
# そのため、各実行で使いまわしたいものはこの中で定義してglobalしておくとよいです。
# 例) Logger, sql_connector, ml model
def initializer(context):
    # Get Logger
    global logger
    logger = logging.getLogger()
    logger.info('initializing')

    # Load Model and Scaler
    global model
    global scaler
    logger.info('Model Loading')
    model = tf.keras.models.load_model('model_path')
    logger.info('Model Loaded')
    logger.info('Scaler Loading')
    scaler = pickle.load(open('scaler_path', 'rb'))
    logger.info('Scaler Loaded')

# メインの処理関数
# リクエスト都度実行される(HTTP Triggerの場合形式が異なるので注意)
def handler(event, context):
    logger.info(event)

    # unctionやServiceに紐付けたRAMで許可されたAlibabaCloudサービスへの
    # アクセスのためのSTS Credentialを取得します
    evt = json.loads(event)
    creds = context.credentials

    accessKeyId = creds.access_key_id
    accessKeySecret = creds.access_key_secret
    securityToken = creds.security_token

    endpoint = evt["source"]["endpoint"]
    project = evt["source"]["projectName"]
    logstore = evt["source"]["logstoreName"]

    # Do your self!!

    return 'hello world' # 適切なreturnに置き換えること
