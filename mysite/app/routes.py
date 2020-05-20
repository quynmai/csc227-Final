from flask import render_template, request
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/nexus')
def nexus():
    pod_list = read_split('nexus')
    pod_dict = pod_dictionary(pod_list)

    return render_template('nexus.html', title='Nexus Topologies', pod_list=pod_list, pod_dict=pod_dict)


@app.route('/asr')
def asr():
    pod_list = read_split('asr')
    pod_dict = pod_dictionary(pod_list)

    return render_template('asr.html', title='ASR Topologies', pod_list=pod_list, pod_dict=pod_dict)


@app.route('/catalyst')
def catalyst():
    pod_list = read_split('catalyst')
    pod_dict = pod_dictionary(pod_list)

    return render_template('catalyst.html', title='Catalyst Topologies', pod_list=pod_list, pod_dict=pod_dict)


@app.route('/firepower')
def firepower():
    pod_list = read_split('firepower')
    pod_dict = pod_dictionary(pod_list)

    return render_template('firepower.html', title='Firepower Topologies', pod_list=pod_list, pod_dict=pod_dict)


@app.route('/alltopos')
def alltopos():
    pod_list = read_split('all_pod_types')
    pod_dict = pod_dictionary(pod_list)

    return render_template('alltopos.html', title='All Topologies', pod_list=pod_list, pod_dict=pod_dict)


@app.route('/podsearch', methods=['GET', 'POST'])
def podsearch():
    if request.method == 'POST':
        devices_list = request.form.get('devices').split()
        pod_list = search_device(devices_list)
        pod_dict = pod_dictionary(pod_list)

        return render_template('podsearch.html', title='Search Topologies by Device', pod_list=pod_list,
                               pod_dict=pod_dict)

    return render_template('podsearch.html', title='Search Topologies by Device', pod_list="", pod_dict="")


def search_device(devices_list):
    pod_list = []

    # read in file
    file = open('/home/csc227/mysite/static/pod_info/SJ_pod_info_cleaned.csv', 'r')

    for device in devices_list:
        for line in file:
            device_info_list = line.strip().split(',')  # Get device info into list
            pod = device_info_list[0].strip()
            device_name = device_info_list[3].strip()

            if (device_name.find(device.upper()) != -1) and (pod not in pod_list):
                pod_list.append(pod)

    # close the opened file
    file.close()

    return pod_list


# returns the pod numbers in a list form for each of the text files specified
def read_split(type):
    pod_list = []
    file = open('/home/csc227/mysite/static/pod_info/{}.txt'.format(type), 'r')
    for line in file:
        pod_list.append(line.strip())
    file.close()
    return pod_list


def create_device_dict_from_pod_num(pod_num):
    file = open('/home/csc227/mysite/static/pod_info/SJ_pods.csv', 'r')

    # Dictionary of all the devices; key=device_id; values=pod, pod_name, device_name, itm
    device_list = []
    device_dict = {}

    for line in file:
        device_info_list = line.strip().split(',')  # Get device info into list
        pod = device_info_list[0].strip()
        pod_name = device_info_list[1].strip()
        device_name = device_info_list[3].strip()

        if (pod_num == pod):
            device_dict.update({'pod_name': pod_name})
            device_list.append(device_name)

    device_dict.update({'devices': device_list})

    # close the opened file
    file.close()

    return device_dict


def pod_dictionary(pod_list):
    pod_dict = {}
    for pod in pod_list:
        device_dict = create_device_dict_from_pod_num(pod)
        pod_dict.update({pod: device_dict})

    return pod_dict

