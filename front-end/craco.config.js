module.exports = {
    webpack: {
      configure: (webpackConfig) => {
        webpackConfig.plugins = webpackConfig.plugins.filter(
          (plugin) => plugin.constructor.name !== "ForkTsCheckerWebpackPlugin"
        );
        return webpackConfig;
      },
    },
  };
  