import json
import logging
import os
import socket
import socketserver
from dataclasses import is_dataclass
from socketserver import StreamRequestHandler
from typing import Optional

from stem.envelope import Envelope
from stem.task_master import TaskMaster
from stem.task_runner import SimpleRunner
from stem.task_tree import TaskTree
from stem.workspace import IWorkspace
from multiprocessing import Process

from tests.example_tasks import int_range


class UnitHandler(StreamRequestHandler):
    workspace: IWorkspace
    task_tree: TaskTree = TaskTree(int_range)
    task_master = TaskMaster(SimpleRunner(), task_tree)
    powerfullity: int

    def handle(self) -> Envelope:
        data = Envelope.read(self.rfile)
        print(data.data.decode('utf-8').replace("'", "\""))
        print(data.meta)
        meta = data.meta
        meta_data = data.data.decode('utf-8').replace("'", "\"")
        if meta_data == '':
            meta_data = {}
        else:
            meta_data = eval(meta_data)
        if 'command' in meta:
            com_value = meta['command']
            match com_value:
                case 'run':
                    if 'task_path' in meta_data:
                        task_master = TaskMaster(SimpleRunner())
                        task = UnitHandler.workspace.find_task(meta_data['task_path'])
                        result = task_master.execute(meta, task)
                        self.wfile.write(Envelope({'task_result': result}).to_bytes())
                case 'structure':
                    self.wfile.write(
                        Envelope(UnitHandler.workspace.structure()).to_bytes())
                case 'powerfullity':
                    self.wfile.write(
                        Envelope({'powerfullity': UnitHandler.powerfullity}).to_bytes())
                # case 'stop':
                #     self.finish()
        else:
            self.wfile.write(Envelope({'status': 'failed', 'error': 'KeyError: command'}).to_bytes())


def start_unit(workspace: IWorkspace, host: str, port: int, powerfullity: Optional[int] = None):
    UnitHandler.powerfullity = powerfullity
    UnitHandler.workspace = workspace
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((host, port), UnitHandler) as server:
        server.serve_forever()


def start_unit_in_subprocess(workspace: IWorkspace, host: str, port: int,
                             powerfullity: Optional[int] = None) -> Process:
    my_thread = Process(target=start_unit, args=(workspace, host, port, powerfullity))
    return my_thread
