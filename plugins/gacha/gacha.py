# encoding:utf-8

import random

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *


@plugins.register(name="Gacha", desc="一个可以模拟抽卡的插件", version="0.1", author="mage", desire_priority= 10)
class Gacha(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        self.initMap = {}
        self.reward_Map = {}
        self.devider="\n---💗---\n"
        logger.info("[Hello] inited")
    
    def reward(self):
        list = []
        for k in self.initMap:
            list.append(f"奖品: {k} 数量: {self.initMap[k]}")
        return "\n".join(list)

    def my_reward(self):
        list = []
        for k in self.reward_Map:
            list.append(f"{k}:{self.reward_Map[k]}")
        return "\n".join(list)

    def on_handle_context(self, e_context: EventContext):

        if e_context['context'].type != ContextType.TEXT:
            return
        
        content = e_context['context'].content
        logger.debug("[Hello] on_handle_context. content: %s" % content)
        clist = e_context['context'].content.split(maxsplit=1)


        if clist[0]== "$clear":
            reply = Reply()
            reply.type = ReplyType.TEXT
            self.reward_Map = {}
            self.initMap = {}
            reply.content="清空奖品奖池成功"
            e_context['reply']= reply
            e_context.action = EventAction.BREAK_PASS # 事件结束，并跳过处理context的默认逻辑
        
        if clist[0]== "$set":
            reply = Reply()
            reply.type = ReplyType.TEXT
            for v in clist[1]:
                key = v.split(":")[0]
                value = v.split(":")[1]
                self.reward_Map = {}
                self.reward_Map[key] = value
            reply.content="更新我的奖品 成功，当前奖品: \n " + self.my_reward()()
            e_context['reply']= reply
            e_context.action = EventAction.BREAK_PASS # 事件结束，并跳过处理context的默认逻辑


        if clist[0]== "$add":
            reply = Reply()
            reply.type = ReplyType.TEXT
            for v in clist[1].split("\n"):
                key = v.split(":")[0]
                value = int(v.split(":")[1])
                if key in self.initMap:
                    self.initMap[key]+=value
                else:
                    self.initMap[key] = value
            reply.content="更新奖池 成功，当前奖品: \n " + self.reward()
            e_context['reply']= reply
            e_context.action = EventAction.BREAK_PASS # 事件结束，并跳过处理context的默认逻辑

        if content == "十连抽":
            reply = Reply()
            reply.type = ReplyType.TEXT
            pool=[]
            ret=[]
            for k in self.initMap:
                v = self.initMap[k]
                pool+=[k]* int(v)
            for _ in range(10):
                x = random.choice(pool)
                ret.append(f"恭喜您，抽中 {x}")
                pool.remove(x)
                self.initMap[x] -= 1
                if x in self.reward_Map:
                    self.reward_Map+=1
                else:
                    self.reward_Map=1

            reply.content = "抽奖结束\n" + "\n".join(ret) + self.devider + "剩余奖品:\n" +self.reward()+self.devider + "您抽中的奖品："+self.my_reward()
            e_context['reply'] = reply
            e_context.action = EventAction.BREAK_PASS


    def get_help_text(self, **kwargs):
        help_text = "抽奖模拟器~ 0.1版本\n"
        return help_text
