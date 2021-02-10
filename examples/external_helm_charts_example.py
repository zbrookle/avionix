from avionix import ChartBuilder, ChartDependency, ChartInfo

if __name__ == "__main__":
    builder = ChartBuilder(
        ChartInfo(
            api_version="3.2.4",
            name="my_chart",
            version="0.1.0",
            app_version="v1",
            dependencies=[
                ChartDependency(
                    "grafana",
                    "5.5.2",
                    "https://charts.helm.sh/stable",
                    "stable",
                    values={"resources": {"requests": {"memory": "100Mi"}}},
                ),
                ChartDependency(
                    "local-chart",
                    "0.1.0",
                    "file:///path/to/my/local-chart",
                    "local-repo",
                    is_local=True,
                ),
            ],
        ),
        [],
    )
    builder.install_chart({"dependency-update": None})
