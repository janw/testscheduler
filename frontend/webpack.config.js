const path = require('path');
const merge = require('webpack-merge');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const devMode = process.env.NODE_ENV !== 'production';

const baseConfig = {
  context: path.resolve(__dirname, 'src'),
  entry: {
    app: './app.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[hash:8].js',
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: (file) => /node_modules/.test(file) && !/\.vue\.js/.test(file),
      },
      {
        test: /\.s?[ac]ss$/,
        use: ['style-loader', 'vue-style-loader', 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'img/',
              esModule: false,
            },
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.vue', '.js'],
    alias: {
      vue: 'vue/dist/vue.js',
    },
  },
  plugins: [
    new HtmlWebpackPlugin({
      inject: false,
      title: 'Test Executor',
      template: './template.html',
    }),
    new VueLoaderPlugin(),
  ],
  performance: {
    hints: false,
  },
};

const devConfig = {
  mode: 'development',
  devtool: 'source-map',
  devServer: {
    sockPath: '/__webpacksock',
    contentBase: path.join(__dirname, 'dist'),
    compress: false,
    port: 9000,
    proxy: [
      {
        context: ['/api', '/sock'],
        target: 'http://localhost:5000',
        ws: true
      },
    ],
  },
};

const prodConfig = {
  mode: 'production',
  output: {
    publicPath: '/static/',
  },
  resolve: {
    alias: {
      vue: 'vue/dist/vue.min.js',
    },
  },
};

module.exports = merge(baseConfig, devMode ? devConfig : prodConfig);
