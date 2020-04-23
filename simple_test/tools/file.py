def YamlConfigLoader(configFile):
    import yaml
    with open(configFile, encoding="UTF-8") as f:
        return yaml.load(f, Loader=yaml.CLoader)
