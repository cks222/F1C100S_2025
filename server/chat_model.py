# from Phi3 import Phi
# from llama31b import Llama321b
from openai import OpenAI
import asyncio
import random


class MyModel:
    def __init__(self, baseurl, modelid):
        api_key = "a827ca8d-8be4-4d31-b856-76c5a9f5073f"
        self.model_id = modelid
        self.client = OpenAI(
            base_url=f"https://{baseurl}.api-inference.modelscope.cn/v1",
            api_key=api_key,
        )

    def CreateChatCompletions(self, messages):
        return self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            stream=True,
        )


class MyChatModel:
    def __init__(self):
        self.Concurrency = 5
        self.models = [
            MyModel("ms-fc-9f87b9d0-5155", "Qwen/Qwen2.5-0.5B-Instruct-GGUF"),
            MyModel("ms-fc-4391cc7c-5bb0", "Qwen/Qwen2.5-0.5B-Instruct-GGUF"),
            MyModel("ms-fc-59d43fda-f106", "LLM-Research/phi-4-gguf"),
            MyModel("ms-fc-6c45a216-5670", "Qwen/Qwen2.5-3B-Instruct-GGUF"),
        ]
        self.busyModelIndex = [0 for i in range(len(self.models))]

    def getFreeModels(self):
        return sorted(
            range(len(self.busyModelIndex)), key=lambda x: self.busyModelIndex[x]
        )[: self.Concurrency]

    def Chat(self, messages):
        result = ""
        for chunk in self.models[0].CreateChatCompletions(messages):
            result = result + chunk.choices[0].delta.content
        return result

    async def Chat_Stream(self, messages):
        tasks = [
            asyncio.create_task(self.SelecFastestResponse(i, messages))
            for i in self.getFreeModels()
        ]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()
        for chunk in done.pop().result():
            print(chunk.choices[0].delta.content)
            yield chunk.choices[0].delta.content
            await asyncio.sleep(0)

        yield "[end]"
        await asyncio.sleep(0)

    async def SelecFastestResponse(self, i, messages):
        self.busyModelIndex[i] = self.busyModelIndex[i] + 1
        response = self.models[i].CreateChatCompletions(messages)
        self.busyModelIndex[i] = self.busyModelIndex[i] - 1
        print(self.models[i].model_id)
        return response

    def test(self):
        messages = [{"role": "user", "content": "你好，能帮我介绍一下杭州吗？"}]
        result = self.Chat(messages)
        print(result)


if __name__ == "__main__":
    s = MyChatModel()
    s.test()
