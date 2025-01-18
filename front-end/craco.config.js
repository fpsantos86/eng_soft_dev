module.exports = {
    webpack: {
      configure: (webpackConfig) => {
        console.log("Configurações de Webpack antes:", webpackConfig.plugins);
        webpackConfig.plugins = webpackConfig.plugins.filter(
          (plugin) => plugin.constructor.name !== "ForkTsCheckerWebpackPlugin"
        );
        console.log("Configurações de Webpack depois:", webpackConfig.plugins);
        return webpackConfig;
      },
    },
  };
  