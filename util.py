def save_file(file, output_name):
    output_file = open(output_name, 'wb')
    pickle.dump(file, output_file)
    output_file.close()
    return


def load_file(file_name):
    file = open(file_name, 'rb')
    data = pickle.load(file)
    file.close()
    return data