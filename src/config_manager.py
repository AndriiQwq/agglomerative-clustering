class ConfigManager:
    def __init__(self):
        self.config = {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def load_ini_config(self, config_file):
        """
        Loads configuration from a .ini file with key: value pairs.
        """
        import os
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")
        with open(config_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or ':' not in line:
                continue
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Clustering Configuration
            if key == '[centroid-1, medoid-2]':
                self.config['mode'] = int(value)
            elif key == 'Linkage[1 - single, 2 - average]':
                self.config['linkage'] = int(value)

            # Clusters count
            elif key == 'Count_of_first_points':
                self.config['size_of_first_points'] = int(value)
            elif key == 'Count_of_points':
                self.config['size_of_points_to_generate'] = int(value)

            # Program settings
            elif key == 'Logout':
                self.config['logout'] = value.lower() == 'on'
            elif key == 'Text output':
                self.config['text_output'] = value.lower() == 'on'

            # Map size
            elif key == 'x_min':
                self.config['x_min'] = int(value)
            elif key == 'x_max':
                self.config['x_max'] = int(value)
            elif key == 'y_min':
                self.config['y_min'] = int(value)
            elif key == 'y_max':
                self.config['y_max'] = int(value)

            # Offset for points
            elif key == 'X_offset_min':
                self.config['X_offset_min'] = int(value)
            elif key == 'X_offset_max':
                self.config['X_offset_max'] = int(value)
            elif key == 'Y_offset_min':
                self.config['Y_offset_min'] = int(value)
            elif key == 'Y_offset_max':
                self.config['Y_offset_max'] = int(value)
