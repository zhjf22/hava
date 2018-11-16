var Mission = function () {
    this.id = 0;
    this.remote_ip = "";
    this.user = "";
    this.password = "";
    this.node = "";
    this.permission = "";
    this.config = "";
    this.createTS = "";

    this.toJSON = function () {
        return {
            "remote_ip":this.remote_ip,
            "id": this.id,
            "user": this.user,
            "password": this.password,
            "node": this.node,
            "permission": this.permission,
            "config": this.config,
            "createTS": this.createTS
        };
    }
};

Mission.fromJSON = function (o) {
    var mission = new Mission();
    mission.id = o["id"];
    mission.user = o["user"];
    mission.password = o["password"];
    mission.node = o["node"];
    mission.permission = o["permission"];
    mission.config = o["config"];
    mission.createTS = o["createTS"];
    return mission;
};
