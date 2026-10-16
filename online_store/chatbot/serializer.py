from rest_framework.serializers import ModelSerializer
from .models import chat, ChatMessage
from google import genai
from google.genai import types
import os
from online_store.settings.dev import *
from .tools import *

system_prompt = "if the user asked about a specific product, extract the provided parameters, structure them as max_price and name, if the user didn't provide anyone of them, replace it with None "
client = genai.Client(api_key=genai_key)
chat_model = client.chats.create(model="gemini-2.5-flash", config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[search_products, get_recommendations],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    ),)

FUNCTION_MAP = {
    "search_products": search_products,
    "get_recommendations": get_recommendations,
}

class chat_serializer(ModelSerializer):
    class Meta:
        model = chat
        fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return chat.objects.create(**validated_data)


class ChatMessage_serializer(ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = ['message', 'response']

    def create(self, validated_data):
        message = validated_data['message']

        chat_pk = self.context["view"].kwargs.get("chat_pk")

        chat_object = chat.objects.get(pk=chat_pk)
        response = chat_model.send_message(message)
        part = response.candidates[0].content.parts[0]

        if part.function_call:
            # It's a structured call, not text
            func_name = part.function_call.name
            func_args = dict(part.function_call.args)   # already a real dict, no parsing needed

            result = FUNCTION_MAP[func_name](**func_args)  # run your Django/ORM logic

            # send the result back so Gemini can phrase a natural reply
            follow_up = chat_model.send_message(
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": result}
                )
            )
            reply_text = follow_up.text
        else:
            reply_text = part.text

        validated_data['chat'] = chat_object
        validated_data['response'] = reply_text
        return ChatMessage.objects.create(**validated_data)