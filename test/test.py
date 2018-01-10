import os.path
import subprocess

def get_tool_path(tool):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "epigeec", "python", "core", tool)

def launch_to_hdf5(list_path, conf_path):
    tool_path = get_tool_path("bw_to_hdf5.py")
    subprocess.call(["python", tool_path, list_path, conf_path])

def launch_filter(list_path, conf_path):
    tool_path = get_tool_path("filter_hdf5.py")
    subprocess.call(["python", tool_path, list_path, conf_path])

def launch_corr(list_path, conf_path):
    tool_path = get_tool_path("geec_corr.py")
    subprocess.call(["python", tool_path, list_path, conf_path])

def main():
    test_dir = os.path.dirname(__file__)
    conf_path = os.path.join(test_dir, "files", "test.conf")
    template_path = os.path.join(test_dir, "template.conf")
    list_path = os.path.join(test_dir, "test_list.txt")

    open(conf_path, 'w').write(open(template_path).read().replace("__file__", test_dir))

    launch_to_hdf5(list_path, conf_path)
    launch_filter(list_path, conf_path)
    launch_corr(list_path, conf_path)


if __name__ == "__main__":
    main()
