#!/usr/bin/enc python

"""Сценарий динамического реестра Ansible с использованием Vagrant"""

import sys
import json
import argparse
import subprocess

import chardet
import paramiko


def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Сценарий динамического реестра Vagrant")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()


def check_output(command: str) -> str:
    """Выполняет переданную команду в командной оболочке и возвращает результат"""
    command = command.split(' ')
    raw_result_command = subprocess.check_output(command).rstrip()
    encoding_result = chardet.detect(raw_result_command)['encoding']
    return raw_result_command.decode(encoding_result)


def list_running_hosts():
    """Возвращает информацию о хостах"""
    command = "vagrant status --machine-readable"
    data = check_output(command)
    hosts = []
    for line in data.split('\n'):
        (_, host, key, value) = line.split()
        if key == 'state' and value == 'running':
            hosts.append(host)
    
    return hosts
    
def get_host_details(host):
    """Выводит инофрмацию о хостах"""
    command = f"vagrant ssh-config {host}"
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    config = paramiko.SSHConfig()
    c = config.lookup(host)
    return {'ansible_ssh_host': c['hostname'],
            'ansible_ssh_port': c['port'],
            'ansible_ssh_user': c['user'],
            'ansible_ssh_private_key_file': c['identityfile'][0],}
            

def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump({'vagrant': hosts}, sys.stodut)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)


if __name__ == '__main__':
   main()