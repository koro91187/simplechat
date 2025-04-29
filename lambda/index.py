import json
import os
import urllib.request

# FastAPIサーバーのURL
FASTAPI_ENDPOINT = os.environ.get("FASTAPI_ENDPOINT", "https://ff01-34-126-136-109.ngrok-free.app/predict")

def lambda_handler(event, context):
    try:
        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])

        print("Sending message to FastAPI:", message)

        # FastAPIサーバーに送るリクエストボディ
        payload = json.dumps({
            "message": message,
            "conversationHistory": conversation_history
        }).encode('utf-8')

        # リクエスト設定
        req = urllib.request.Request(
            FASTAPI_ENDPOINT,
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        # リクエストを送る
        with urllib.request.urlopen(req) as res:
            response_body = res.read()
        
        response_json = json.loads(response_body)
        print("FastAPI response:", response_json)

        # FastAPI側から返ってきたアシスタントの応答を使う
        assistant_response = response_json['response']
        updated_conversation_history = response_json['conversationHistory']

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": updated_conversation_history
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
