{
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 2,
      "id": "pE2V6v0b4z0T",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "pE2V6v0b4z0T",
        "outputId": "5fffdca5-e55b-4c60-e64c-deadfbd1b45c"
      },
      "outputs": [],
      "source": [
        "!pip install streamlit geopandas pandas_geojson folium numpy panel pandas matplotlib pip"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "KLvULLV65AWJ",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KLvULLV65AWJ",
        "outputId": "49307788-f099-423e-9762-0d0ca4bfc9c3"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/\n",
            "Requirement already satisfied: pip in /usr/local/lib/python3.9/dist-packages (22.0.4)\n",
            "Collecting pip\n",
            "  Downloading pip-23.0.1-py3-none-any.whl (2.1 MB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m2.1/2.1 MB\u001b[0m \u001b[31m23.5 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: pip\n",
            "  Attempting uninstall: pip\n",
            "    Found existing installation: pip 22.0.4\n",
            "    Uninstalling pip-22.0.4:\n",
            "      Successfully uninstalled pip-22.0.4\n",
            "Successfully installed pip-23.0.1\n"
          ]
        }
      ],
      "source": [
        "!pip install --upgrade pip"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "y3de5v-5UvzR",
      "metadata": {
        "id": "y3de5v-5UvzR"
      },
      "source": [
        "Compress function"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "id": "01df2b59-d78e-4753-97c9-1a3a24030181",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 17
        },
        "id": "01df2b59-d78e-4753-97c9-1a3a24030181",
        "outputId": "7af4f79b-11b7-4db5-94a8-80c7c3b3ba8d"
      },
      "outputs": [
        {
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'folium'",
          "output_type": "error",
          "traceback": [
            "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "Cell \u001b[1;32mIn[1], line 1\u001b[0m\n\u001b[1;32m----> 1\u001b[0m \u001b[39mimport\u001b[39;00m \u001b[39mfolium\u001b[39;00m \u001b[39mas\u001b[39;00m \u001b[39mfm\u001b[39;00m\n\u001b[0;32m      2\u001b[0m \u001b[39mfrom\u001b[39;00m \u001b[39mfolium\u001b[39;00m \u001b[39mimport\u001b[39;00m plugins\n\u001b[0;32m      3\u001b[0m \u001b[39mfrom\u001b[39;00m \u001b[39mpandas_geojson\u001b[39;00m \u001b[39mimport\u001b[39;00m read_geojson, filter_geojson\n",
            "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'folium'"
          ]
        }
      ],
      "source": [
        "import folium as fm\n",
        "from folium import plugins\n",
        "from pandas_geojson import read_geojson, filter_geojson\n",
        "import numpy as np\n",
        "import panel as pn\n",
        "pn.extension(sizing_mode=\"stretch_width\")\n",
        "import geopandas as gpd\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import json\n",
        "import urllib.request\n",
        "\n",
        "def create_app2(sociodemo, geo_json, select):\n",
        "    selectv = select.value\n",
        "    filter = [selectv]\n",
        "    selectgeo = filter_geojson(geo_json=geo_json, filter_list=filter, property_key='dun')\n",
        "\n",
        "    # create map object\n",
        "    map = fm.Map(location=[5.016806622688496, 107.9456777002687], tiles='cartodbpositron', zoom_start=6)\n",
        "\n",
        "    # add tool measure to the top right\n",
        "    # from folium.plugins import MeasureControl\n",
        "    # map.add_child(MeasureControl())\n",
        "\n",
        "    # add geojson to map\n",
        "    fm.GeoJson(selectgeo, name='DUN boundary', tooltip=fm.GeoJsonTooltip(fields=['dun', 'parlimen'])).add_to(map)\n",
        "    map.fit_bounds(map.get_bounds(), padding=(30, 30))\n",
        "    folium_map = pn.panel(map, height=400)\n",
        "\n",
        "    # select data based on selected value\n",
        "    select_sociodemo = sociodemo[sociodemo['dun'] == selectv]\n",
        "\n",
        "    # round watercover to 3 decimal places\n",
        "    select_sociodemo['watercover'] = np.round(select_sociodemo.watercover, decimals=3)\n",
        "\n",
        "    # get max_elevation, watercover and population_total\n",
        "    max_elev = select_sociodemo['max_elevation'].iloc[0]\n",
        "    water = select_sociodemo['watercover'].iloc[0]\n",
        "    pop = select_sociodemo['population_total'].iloc[0]\n",
        "\n",
        "    # create indicators\n",
        "    number = pn.indicators.Number(format='{value}')\n",
        "\n",
        "    indicator = pn.Row(\n",
        "        number.clone(name='Population', value=pop, colors=[(33, 'black')]),\n",
        "        number.clone(name='Maximum Elevation', value=max_elev, colors=[(66, 'blue')]),\n",
        "        number.clone(name='Surface covered in water', value=water, colors=[(100, 'red')]),\n",
        "        sizing_mode='stretch_width')\n",
        "\n",
        "    # create description\n",
        "    description = select_sociodemo['dun'].iloc[0]\n",
        "    str_pane = pn.indicators.Number(name=str(description))\n",
        "\n",
        "    # create panel object\n",
        "    app2 = pn.Column(\n",
        "        pn.Column(\n",
        "            str_pane,\n",
        "            indicator,\n",
        "            folium_map,\n",
        "            sizing_mode='scale_both'\n",
        "        ),\n",
        "        sizing_mode='scale_both'\n",
        "    )\n",
        "\n",
        "    return app2\n"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "_c-IM6ihkOOV",
      "metadata": {
        "id": "_c-IM6ihkOOV"
      },
      "source": [
        "Select option"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "1fnQy5DiR0d1",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 78
        },
        "id": "1fnQy5DiR0d1",
        "outputId": "b5771043-fdf0-44d9-92eb-a32916660616"
      },
      "outputs": [
        {
          "data": {
            "application/javascript": "(function(root) {\n  function now() {\n    return new Date();\n  }\n\n  var force = true;\n\n  if (typeof root._bokeh_onload_callbacks === \"undefined\" || force === true) {\n    root._bokeh_onload_callbacks = [];\n    root._bokeh_is_loading = undefined;\n  }\n\n  if (typeof (root._bokeh_timeout) === \"undefined\" || force === true) {\n    root._bokeh_timeout = Date.now() + 5000;\n    root._bokeh_failed_load = false;\n  }\n\n  function run_callbacks() {\n    try {\n      root._bokeh_onload_callbacks.forEach(function(callback) {\n        if (callback != null)\n          callback();\n      });\n    } finally {\n      delete root._bokeh_onload_callbacks\n    }\n    console.debug(\"Bokeh: all callbacks have finished\");\n  }\n\n  function load_libs(css_urls, js_urls, js_modules, callback) {\n    if (css_urls == null) css_urls = [];\n    if (js_urls == null) js_urls = [];\n    if (js_modules == null) js_modules = [];\n\n    root._bokeh_onload_callbacks.push(callback);\n    if (root._bokeh_is_loading > 0) {\n      console.debug(\"Bokeh: BokehJS is being loaded, scheduling callback at\", now());\n      return null;\n    }\n    if (js_urls.length === 0 && js_modules.length === 0) {\n      run_callbacks();\n      return null;\n    }\n    console.debug(\"Bokeh: BokehJS not loaded, scheduling load and callback at\", now());\n\n    function on_load() {\n      root._bokeh_is_loading--;\n      if (root._bokeh_is_loading === 0) {\n        console.debug(\"Bokeh: all BokehJS libraries/stylesheets loaded\");\n        run_callbacks()\n      }\n    }\n\n    function on_error() {\n      console.error(\"failed to load \" + url);\n    }\n\n    for (var i = 0; i < css_urls.length; i++) {\n      var url = css_urls[i];\n      const element = document.createElement(\"link\");\n      element.onload = on_load;\n      element.onerror = on_error;\n      element.rel = \"stylesheet\";\n      element.type = \"text/css\";\n      element.href = url;\n      console.debug(\"Bokeh: injecting link tag for BokehJS stylesheet: \", url);\n      document.body.appendChild(element);\n    }\n\n    var skip = [];\n    if (window.requirejs) {\n      window.requirejs.config({'packages': {}, 'paths': {'gridstack': 'https://cdn.jsdelivr.net/npm/gridstack@4.2.5/dist/gridstack-h5', 'notyf': 'https://cdn.jsdelivr.net/npm/notyf@3/notyf.min'}, 'shim': {'gridstack': {'exports': 'GridStack'}}});\n      require([\"gridstack\"], function(GridStack) {\n\twindow.GridStack = GridStack\n\ton_load()\n      })\n      require([\"notyf\"], function() {\n\ton_load()\n      })\n      root._bokeh_is_loading = css_urls.length + 2;\n    } else {\n      root._bokeh_is_loading = css_urls.length + js_urls.length + js_modules.length;\n    }    if (((window['GridStack'] !== undefined) && (!(window['GridStack'] instanceof HTMLElement))) || window.requirejs) {\n      var urls = ['https://cdn.holoviz.org/panel/0.14.4/dist/bundled/gridstack/gridstack@4.2.5/dist/gridstack-h5.js'];\n      for (var i = 0; i < urls.length; i++) {\n        skip.push(urls[i])\n      }\n    }    if (((window['Notyf'] !== undefined) && (!(window['Notyf'] instanceof HTMLElement))) || window.requirejs) {\n      var urls = ['https://cdn.holoviz.org/panel/0.14.4/dist/bundled/notificationarea/notyf@3/notyf.min.js'];\n      for (var i = 0; i < urls.length; i++) {\n        skip.push(urls[i])\n      }\n    }    for (var i = 0; i < js_urls.length; i++) {\n      var url = js_urls[i];\n      if (skip.indexOf(url) >= 0) {\n\tif (!window.requirejs) {\n\t  on_load();\n\t}\n\tcontinue;\n      }\n      var element = document.createElement('script');\n      element.onload = on_load;\n      element.onerror = on_error;\n      element.async = false;\n      element.src = url;\n      console.debug(\"Bokeh: injecting script tag for BokehJS library: \", url);\n      document.head.appendChild(element);\n    }\n    for (var i = 0; i < js_modules.length; i++) {\n      var url = js_modules[i];\n      if (skip.indexOf(url) >= 0) {\n\tif (!window.requirejs) {\n\t  on_load();\n\t}\n\tcontinue;\n      }\n      var element = document.createElement('script');\n      element.onload = on_load;\n      element.onerror = on_error;\n      element.async = false;\n      element.src = url;\n      element.type = \"module\";\n      console.debug(\"Bokeh: injecting script tag for BokehJS library: \", url);\n      document.head.appendChild(element);\n    }\n    if (!js_urls.length && !js_modules.length) {\n      on_load()\n    }\n  };\n\n  function inject_raw_css(css) {\n    const element = document.createElement(\"style\");\n    element.appendChild(document.createTextNode(css));\n    document.body.appendChild(element);\n  }\n\n  var js_urls = [\"https://cdn.bokeh.org/bokeh/release/bokeh-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-gl-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-widgets-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-mathjax-2.4.3.min.js\", \"https://unpkg.com/@holoviz/panel@0.14.4/dist/panel.min.js\"];\n  var js_modules = [];\n  var css_urls = [\"https://cdn.holoviz.org/panel/0.14.4/dist/css/widgets.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/loading.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/alerts.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/debugger.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/json.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/card.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/dataframe.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/markdown.css\"];\n  var inline_js = [    function(Bokeh) {\n      inject_raw_css(\"\\n    .bk.pn-loading.arc:before {\\n      background-image: url(\\\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\\\");\\n      background-size: auto calc(min(50%, 400px));\\n    }\\n    \");\n    },    function(Bokeh) {\n      Bokeh.set_log_level(\"info\");\n    },\nfunction(Bokeh) {} // ensure no trailing comma for IE\n  ];\n\n  function run_inline_js() {\n    if ((root.Bokeh !== undefined) || (force === true)) {\n      for (var i = 0; i < inline_js.length; i++) {\n        inline_js[i].call(root, root.Bokeh);\n      }} else if (Date.now() < root._bokeh_timeout) {\n      setTimeout(run_inline_js, 100);\n    } else if (!root._bokeh_failed_load) {\n      console.log(\"Bokeh: BokehJS failed to load within specified timeout.\");\n      root._bokeh_failed_load = true;\n    }\n  }\n\n  if (root._bokeh_is_loading === 0) {\n    console.debug(\"Bokeh: BokehJS loaded, going straight to plotting\");\n    run_inline_js();\n  } else {\n    load_libs(css_urls, js_urls, js_modules, function() {\n      console.debug(\"Bokeh: BokehJS plotting callback run at\", now());\n      run_inline_js();\n    });\n  }\n}(window));",
            "application/vnd.holoviews_load.v0+json": ""
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {
            "application/javascript": "\nif ((window.PyViz === undefined) || (window.PyViz instanceof HTMLElement)) {\n  window.PyViz = {comms: {}, comm_status:{}, kernels:{}, receivers: {}, plot_index: []}\n}\n\n\n    function JupyterCommManager() {\n    }\n\n    JupyterCommManager.prototype.register_target = function(plot_id, comm_id, msg_handler) {\n      if (window.comm_manager || ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null))) {\n        var comm_manager = window.comm_manager || Jupyter.notebook.kernel.comm_manager;\n        comm_manager.register_target(comm_id, function(comm) {\n          comm.on_msg(msg_handler);\n        });\n      } else if ((plot_id in window.PyViz.kernels) && (window.PyViz.kernels[plot_id])) {\n        window.PyViz.kernels[plot_id].registerCommTarget(comm_id, function(comm) {\n          comm.onMsg = msg_handler;\n        });\n      } else if (typeof google != 'undefined' && google.colab.kernel != null) {\n        google.colab.kernel.comms.registerTarget(comm_id, (comm) => {\n          var messages = comm.messages[Symbol.asyncIterator]();\n          function processIteratorResult(result) {\n            var message = result.value;\n            console.log(message)\n            var content = {data: message.data, comm_id};\n            var buffers = []\n            for (var buffer of message.buffers || []) {\n              buffers.push(new DataView(buffer))\n            }\n            var metadata = message.metadata || {};\n            var msg = {content, buffers, metadata}\n            msg_handler(msg);\n            return messages.next().then(processIteratorResult);\n          }\n          return messages.next().then(processIteratorResult);\n        })\n      }\n    }\n\n    JupyterCommManager.prototype.get_client_comm = function(plot_id, comm_id, msg_handler) {\n      if (comm_id in window.PyViz.comms) {\n        return window.PyViz.comms[comm_id];\n      } else if (window.comm_manager || ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null))) {\n        var comm_manager = window.comm_manager || Jupyter.notebook.kernel.comm_manager;\n        var comm = comm_manager.new_comm(comm_id, {}, {}, {}, comm_id);\n        if (msg_handler) {\n          comm.on_msg(msg_handler);\n        }\n      } else if ((plot_id in window.PyViz.kernels) && (window.PyViz.kernels[plot_id])) {\n        var comm = window.PyViz.kernels[plot_id].connectToComm(comm_id);\n        comm.open();\n        if (msg_handler) {\n          comm.onMsg = msg_handler;\n        }\n      } else if (typeof google != 'undefined' && google.colab.kernel != null) {\n        var comm_promise = google.colab.kernel.comms.open(comm_id)\n        comm_promise.then((comm) => {\n          window.PyViz.comms[comm_id] = comm;\n          if (msg_handler) {\n            var messages = comm.messages[Symbol.asyncIterator]();\n            function processIteratorResult(result) {\n              var message = result.value;\n              var content = {data: message.data};\n              var metadata = message.metadata || {comm_id};\n              var msg = {content, metadata}\n              msg_handler(msg);\n              return messages.next().then(processIteratorResult);\n            }\n            return messages.next().then(processIteratorResult);\n          }\n        }) \n        var sendClosure = (data, metadata, buffers, disposeOnDone) => {\n          return comm_promise.then((comm) => {\n            comm.send(data, metadata, buffers, disposeOnDone);\n          });\n        };\n        var comm = {\n          send: sendClosure\n        };\n      }\n      window.PyViz.comms[comm_id] = comm;\n      return comm;\n    }\n    window.PyViz.comm_manager = new JupyterCommManager();\n    \n\n\nvar JS_MIME_TYPE = 'application/javascript';\nvar HTML_MIME_TYPE = 'text/html';\nvar EXEC_MIME_TYPE = 'application/vnd.holoviews_exec.v0+json';\nvar CLASS_NAME = 'output';\n\n/**\n * Render data to the DOM node\n */\nfunction render(props, node) {\n  var div = document.createElement(\"div\");\n  var script = document.createElement(\"script\");\n  node.appendChild(div);\n  node.appendChild(script);\n}\n\n/**\n * Handle when a new output is added\n */\nfunction handle_add_output(event, handle) {\n  var output_area = handle.output_area;\n  var output = handle.output;\n  if ((output.data == undefined) || (!output.data.hasOwnProperty(EXEC_MIME_TYPE))) {\n    return\n  }\n  var id = output.metadata[EXEC_MIME_TYPE][\"id\"];\n  var toinsert = output_area.element.find(\".\" + CLASS_NAME.split(' ')[0]);\n  if (id !== undefined) {\n    var nchildren = toinsert.length;\n    var html_node = toinsert[nchildren-1].children[0];\n    html_node.innerHTML = output.data[HTML_MIME_TYPE];\n    var scripts = [];\n    var nodelist = html_node.querySelectorAll(\"script\");\n    for (var i in nodelist) {\n      if (nodelist.hasOwnProperty(i)) {\n        scripts.push(nodelist[i])\n      }\n    }\n\n    scripts.forEach( function (oldScript) {\n      var newScript = document.createElement(\"script\");\n      var attrs = [];\n      var nodemap = oldScript.attributes;\n      for (var j in nodemap) {\n        if (nodemap.hasOwnProperty(j)) {\n          attrs.push(nodemap[j])\n        }\n      }\n      attrs.forEach(function(attr) { newScript.setAttribute(attr.name, attr.value) });\n      newScript.appendChild(document.createTextNode(oldScript.innerHTML));\n      oldScript.parentNode.replaceChild(newScript, oldScript);\n    });\n    if (JS_MIME_TYPE in output.data) {\n      toinsert[nchildren-1].children[1].textContent = output.data[JS_MIME_TYPE];\n    }\n    output_area._hv_plot_id = id;\n    if ((window.Bokeh !== undefined) && (id in Bokeh.index)) {\n      window.PyViz.plot_index[id] = Bokeh.index[id];\n    } else {\n      window.PyViz.plot_index[id] = null;\n    }\n  } else if (output.metadata[EXEC_MIME_TYPE][\"server_id\"] !== undefined) {\n    var bk_div = document.createElement(\"div\");\n    bk_div.innerHTML = output.data[HTML_MIME_TYPE];\n    var script_attrs = bk_div.children[0].attributes;\n    for (var i = 0; i < script_attrs.length; i++) {\n      toinsert[toinsert.length - 1].childNodes[1].setAttribute(script_attrs[i].name, script_attrs[i].value);\n    }\n    // store reference to server id on output_area\n    output_area._bokeh_server_id = output.metadata[EXEC_MIME_TYPE][\"server_id\"];\n  }\n}\n\n/**\n * Handle when an output is cleared or removed\n */\nfunction handle_clear_output(event, handle) {\n  var id = handle.cell.output_area._hv_plot_id;\n  var server_id = handle.cell.output_area._bokeh_server_id;\n  if (((id === undefined) || !(id in PyViz.plot_index)) && (server_id !== undefined)) { return; }\n  var comm = window.PyViz.comm_manager.get_client_comm(\"hv-extension-comm\", \"hv-extension-comm\", function () {});\n  if (server_id !== null) {\n    comm.send({event_type: 'server_delete', 'id': server_id});\n    return;\n  } else if (comm !== null) {\n    comm.send({event_type: 'delete', 'id': id});\n  }\n  delete PyViz.plot_index[id];\n  if ((window.Bokeh !== undefined) & (id in window.Bokeh.index)) {\n    var doc = window.Bokeh.index[id].model.document\n    doc.clear();\n    const i = window.Bokeh.documents.indexOf(doc);\n    if (i > -1) {\n      window.Bokeh.documents.splice(i, 1);\n    }\n  }\n}\n\n/**\n * Handle kernel restart event\n */\nfunction handle_kernel_cleanup(event, handle) {\n  delete PyViz.comms[\"hv-extension-comm\"];\n  window.PyViz.plot_index = {}\n}\n\n/**\n * Handle update_display_data messages\n */\nfunction handle_update_output(event, handle) {\n  handle_clear_output(event, {cell: {output_area: handle.output_area}})\n  handle_add_output(event, handle)\n}\n\nfunction register_renderer(events, OutputArea) {\n  function append_mime(data, metadata, element) {\n    // create a DOM node to render to\n    var toinsert = this.create_output_subarea(\n    metadata,\n    CLASS_NAME,\n    EXEC_MIME_TYPE\n    );\n    this.keyboard_manager.register_events(toinsert);\n    // Render to node\n    var props = {data: data, metadata: metadata[EXEC_MIME_TYPE]};\n    render(props, toinsert[0]);\n    element.append(toinsert);\n    return toinsert\n  }\n\n  events.on('output_added.OutputArea', handle_add_output);\n  events.on('output_updated.OutputArea', handle_update_output);\n  events.on('clear_output.CodeCell', handle_clear_output);\n  events.on('delete.Cell', handle_clear_output);\n  events.on('kernel_ready.Kernel', handle_kernel_cleanup);\n\n  OutputArea.prototype.register_mime_type(EXEC_MIME_TYPE, append_mime, {\n    safe: true,\n    index: 0\n  });\n}\n\nif (window.Jupyter !== undefined) {\n  try {\n    var events = require('base/js/events');\n    var OutputArea = require('notebook/js/outputarea').OutputArea;\n    if (OutputArea.prototype.mime_types().indexOf(EXEC_MIME_TYPE) == -1) {\n      register_renderer(events, OutputArea);\n    }\n  } catch(err) {\n  }\n}\n",
            "application/vnd.holoviews_load.v0+json": ""
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {
            "text/html": [
              "<style>.bk-root, .bk-root .bk:before, .bk-root .bk:after {\n",
              "  font-family: var(--jp-ui-font-size1);\n",
              "  font-size: var(--jp-ui-font-size1);\n",
              "  color: var(--jp-ui-font-color1);\n",
              "}\n",
              "</style>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {},
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {
            "application/vnd.holoviews_exec.v0+json": "",
            "text/html": [
              "<div id='1036'>\n",
              "  <div class=\"bk-root\" id=\"d408f958-2a91-4b67-979e-684e33b5d6b0\" data-root-id=\"1036\"></div>\n",
              "</div>\n",
              "<script type=\"application/javascript\">(function(root) {\n",
              "  function embed_document(root) {\n",
              "    var docs_json = {\"23c421ca-5e5c-480e-b043-a9d6fa2a10e4\":{\"defs\":[{\"extends\":null,\"module\":null,\"name\":\"ReactiveHTML1\",\"overrides\":[],\"properties\":[]},{\"extends\":null,\"module\":null,\"name\":\"FlexBox1\",\"overrides\":[],\"properties\":[{\"default\":\"flex-start\",\"kind\":null,\"name\":\"align_content\"},{\"default\":\"flex-start\",\"kind\":null,\"name\":\"align_items\"},{\"default\":\"row\",\"kind\":null,\"name\":\"flex_direction\"},{\"default\":\"wrap\",\"kind\":null,\"name\":\"flex_wrap\"},{\"default\":\"flex-start\",\"kind\":null,\"name\":\"justify_content\"}]},{\"extends\":null,\"module\":null,\"name\":\"GridStack1\",\"overrides\":[],\"properties\":[{\"default\":\"warn\",\"kind\":null,\"name\":\"mode\"},{\"default\":null,\"kind\":null,\"name\":\"ncols\"},{\"default\":null,\"kind\":null,\"name\":\"nrows\"},{\"default\":true,\"kind\":null,\"name\":\"allow_resize\"},{\"default\":true,\"kind\":null,\"name\":\"allow_drag\"},{\"default\":[],\"kind\":null,\"name\":\"state\"}]},{\"extends\":null,\"module\":null,\"name\":\"click1\",\"overrides\":[],\"properties\":[{\"default\":\"\",\"kind\":null,\"name\":\"terminal_output\"},{\"default\":\"\",\"kind\":null,\"name\":\"debug_name\"},{\"default\":0,\"kind\":null,\"name\":\"clears\"}]},{\"extends\":null,\"module\":null,\"name\":\"NotificationAreaBase1\",\"overrides\":[],\"properties\":[{\"default\":\"bottom-right\",\"kind\":null,\"name\":\"position\"},{\"default\":0,\"kind\":null,\"name\":\"_clear\"}]},{\"extends\":null,\"module\":null,\"name\":\"NotificationArea1\",\"overrides\":[],\"properties\":[{\"default\":[],\"kind\":null,\"name\":\"notifications\"},{\"default\":\"bottom-right\",\"kind\":null,\"name\":\"position\"},{\"default\":0,\"kind\":null,\"name\":\"_clear\"},{\"default\":[{\"background\":\"#ffc107\",\"icon\":{\"className\":\"fas fa-exclamation-triangle\",\"color\":\"white\",\"tagName\":\"i\"},\"type\":\"warning\"},{\"background\":\"#007bff\",\"icon\":{\"className\":\"fas fa-info-circle\",\"color\":\"white\",\"tagName\":\"i\"},\"type\":\"info\"}],\"kind\":null,\"name\":\"types\"}]},{\"extends\":null,\"module\":null,\"name\":\"Notification\",\"overrides\":[],\"properties\":[{\"default\":null,\"kind\":null,\"name\":\"background\"},{\"default\":3000,\"kind\":null,\"name\":\"duration\"},{\"default\":null,\"kind\":null,\"name\":\"icon\"},{\"default\":\"\",\"kind\":null,\"name\":\"message\"},{\"default\":null,\"kind\":null,\"name\":\"notification_type\"},{\"default\":false,\"kind\":null,\"name\":\"_destroyed\"}]},{\"extends\":null,\"module\":null,\"name\":\"TemplateActions1\",\"overrides\":[],\"properties\":[{\"default\":0,\"kind\":null,\"name\":\"open_modal\"},{\"default\":0,\"kind\":null,\"name\":\"close_modal\"}]},{\"extends\":null,\"module\":null,\"name\":\"MaterialTemplateActions1\",\"overrides\":[],\"properties\":[{\"default\":0,\"kind\":null,\"name\":\"open_modal\"},{\"default\":0,\"kind\":null,\"name\":\"close_modal\"}]}],\"roots\":{\"references\":[{\"attributes\":{\"client_comm_id\":\"541abac36ae74d9dbf307e888916736a\",\"comm_id\":\"89e8452587b84321b4885b110c5d6a76\",\"plot_id\":\"1036\"},\"id\":\"1037\",\"type\":\"panel.models.comm_manager.CommManager\"},{\"attributes\":{\"margin\":[5,10,5,10],\"options\":[\"N.01 Penaga\",\"N.02 Bertam\",\"N.03 Pinang Tunggal\",\"N.04 Permatang Berangan\",\"N.05 Sungai Dua\",\"N.06 Telok Ayer Tawar\",\"N.07 Sungai Puyu\",\"N.08 Bagan Jermal\",\"N.09 Bagan Dalam\",\"N.10 Seberang Jaya\",\"N.11 Permatang Pasir\",\"N.12 Penanti\",\"N.13 Berapit\",\"N.14 Machang Bubuk\",\"N.15 Padang Lalang\",\"N.16 Perai\",\"N.17 Bukit Tengah\",\"N.18 Bukit Tambun\",\"N.19 Jawi\",\"N.20 Sungai Bakap\",\"N.21 Sungai Acheh\",\"N.22 Tanjong Bunga\",\"N.23 Air Putih\",\"N.24 Kebun Bunga\",\"N.25 Pulau Tikus\",\"N.26 Padang Kota\",\"N.27 Pengkalan Kota\",\"N.28 Komtar\",\"N.29 Datok Keramat\",\"N.30 Sungai Pinang\",\"N.31 Batu Lancang\",\"N.32 Seri Delima\",\"N.33 Air Itam\",\"N.34 Paya Terubong\",\"N.35 Batu Uban\",\"N.36 Pantai Jerejak\",\"N.37 Batu Maung\",\"N.38 Bayan Lepas\",\"N.39 Pulau Betong\",\"N.40 Telok Bahang\"],\"sizing_mode\":\"stretch_width\",\"title\":\"Select DUN\",\"value\":\"N.01 Penaga\"},\"id\":\"1036\",\"type\":\"panel.models.widgets.CustomSelect\"}],\"root_ids\":[\"1036\",\"1037\"]},\"title\":\"Bokeh Application\",\"version\":\"2.4.3\"}};\n",
              "    var render_items = [{\"docid\":\"23c421ca-5e5c-480e-b043-a9d6fa2a10e4\",\"root_ids\":[\"1036\"],\"roots\":{\"1036\":\"d408f958-2a91-4b67-979e-684e33b5d6b0\"}}];\n",
              "    root.Bokeh.embed.embed_items_notebook(docs_json, render_items);\n",
              "    for (const render_item of render_items) {\n",
              "      for (const root_id of render_item.root_ids) {\n",
              "\tconst id_el = document.getElementById(root_id)\n",
              "\tif (id_el.children.length && (id_el.children[0].className === 'bk-root')) {\n",
              "\t  const root_el = id_el.children[0]\n",
              "\t  root_el.id = root_el.id + '-rendered'\n",
              "\t}\n",
              "      }\n",
              "    }\n",
              "  }\n",
              "  if (root.Bokeh !== undefined && root.Bokeh.Panel !== undefined) {\n",
              "    embed_document(root);\n",
              "  } else {\n",
              "    var attempts = 0;\n",
              "    var timer = setInterval(function(root) {\n",
              "      if (root.Bokeh !== undefined && root.Bokeh.Panel !== undefined) {\n",
              "        clearInterval(timer);\n",
              "        embed_document(root);\n",
              "      } else if (document.readyState == \"complete\") {\n",
              "        attempts++;\n",
              "        if (attempts > 200) {\n",
              "          clearInterval(timer);\n",
              "          console.log(\"Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing\");\n",
              "        }\n",
              "      }\n",
              "    }, 25, root)\n",
              "  }\n",
              "})(window);</script>"
            ],
            "text/plain": [
              "Select(options=['N.01 Penaga', ...], sizing_mode='stretch_width', value='N.01 Penaga')"
            ]
          },
          "execution_count": 32,
          "metadata": {
            "application/vnd.holoviews_exec.v0+json": {
              "id": "1036"
            }
          },
          "output_type": "execute_result"
        }
      ],
      "source": [
        "url = 'https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/electoral_1_dun.geojson'\n",
        "\n",
        "geo_json = json.load(urllib.request.urlopen(url))\n",
        "\n",
        "duns = gpd.read_file(url)\n",
        "\n",
        "sociodemo = pd.read_csv('https://github.com/booluckgmie/podac/raw/main/sociodemo.csv')\n",
        "\n",
        "#READ DATAFRAME\n",
        "from pandas_geojson import read_geojson, filter_geojson\n",
        "filter = ['Pulau Pinang']\n",
        "select = filter_geojson(geo_json=geo_json, filter_list=filter, property_key='state')\n",
        "duns_pp = duns[duns['state'].isin(filter)].reset_index(drop=True)\n",
        "select_options = duns_pp['dun'].values.tolist()\n",
        "\n",
        "#CREATE SELECTION\n",
        "select = pn.widgets.Select(name='Select DUN', options=select_options)\n",
        "select\n"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "-YZnVSDmU-YW",
      "metadata": {
        "id": "-YZnVSDmU-YW"
      },
      "source": [
        "Run apps deploy"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "8Fi2YKUBTI6Q",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 834
        },
        "id": "8Fi2YKUBTI6Q",
        "outputId": "b8d7ac7b-51f4-493c-c7b1-7102d483d372"
      },
      "outputs": [
        {
          "name": "stderr",
          "output_type": "stream",
          "text": [
            "<ipython-input-31-6c41277d8c16>:34: SettingWithCopyWarning: \n",
            "A value is trying to be set on a copy of a slice from a DataFrame.\n",
            "Try using .loc[row_indexer,col_indexer] = value instead\n",
            "\n",
            "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
            "  select_sociodemo['watercover'] = np.round(select_sociodemo.watercover, decimals=3)\n"
          ]
        },
        {
          "data": {
            "application/javascript": "(function(root) {\n  function now() {\n    return new Date();\n  }\n\n  var force = true;\n\n  if (typeof root._bokeh_onload_callbacks === \"undefined\" || force === true) {\n    root._bokeh_onload_callbacks = [];\n    root._bokeh_is_loading = undefined;\n  }\n\n  if (typeof (root._bokeh_timeout) === \"undefined\" || force === true) {\n    root._bokeh_timeout = Date.now() + 5000;\n    root._bokeh_failed_load = false;\n  }\n\n  function run_callbacks() {\n    try {\n      root._bokeh_onload_callbacks.forEach(function(callback) {\n        if (callback != null)\n          callback();\n      });\n    } finally {\n      delete root._bokeh_onload_callbacks\n    }\n    console.debug(\"Bokeh: all callbacks have finished\");\n  }\n\n  function load_libs(css_urls, js_urls, js_modules, callback) {\n    if (css_urls == null) css_urls = [];\n    if (js_urls == null) js_urls = [];\n    if (js_modules == null) js_modules = [];\n\n    root._bokeh_onload_callbacks.push(callback);\n    if (root._bokeh_is_loading > 0) {\n      console.debug(\"Bokeh: BokehJS is being loaded, scheduling callback at\", now());\n      return null;\n    }\n    if (js_urls.length === 0 && js_modules.length === 0) {\n      run_callbacks();\n      return null;\n    }\n    console.debug(\"Bokeh: BokehJS not loaded, scheduling load and callback at\", now());\n\n    function on_load() {\n      root._bokeh_is_loading--;\n      if (root._bokeh_is_loading === 0) {\n        console.debug(\"Bokeh: all BokehJS libraries/stylesheets loaded\");\n        run_callbacks()\n      }\n    }\n\n    function on_error() {\n      console.error(\"failed to load \" + url);\n    }\n\n    for (var i = 0; i < css_urls.length; i++) {\n      var url = css_urls[i];\n      const element = document.createElement(\"link\");\n      element.onload = on_load;\n      element.onerror = on_error;\n      element.rel = \"stylesheet\";\n      element.type = \"text/css\";\n      element.href = url;\n      console.debug(\"Bokeh: injecting link tag for BokehJS stylesheet: \", url);\n      document.body.appendChild(element);\n    }\n\n    var skip = [];\n    if (window.requirejs) {\n      window.requirejs.config({'packages': {}, 'paths': {'gridstack': 'https://cdn.jsdelivr.net/npm/gridstack@4.2.5/dist/gridstack-h5', 'notyf': 'https://cdn.jsdelivr.net/npm/notyf@3/notyf.min'}, 'shim': {'gridstack': {'exports': 'GridStack'}}});\n      require([\"gridstack\"], function(GridStack) {\n\twindow.GridStack = GridStack\n\ton_load()\n      })\n      require([\"notyf\"], function() {\n\ton_load()\n      })\n      root._bokeh_is_loading = css_urls.length + 2;\n    } else {\n      root._bokeh_is_loading = css_urls.length + js_urls.length + js_modules.length;\n    }    if (((window['GridStack'] !== undefined) && (!(window['GridStack'] instanceof HTMLElement))) || window.requirejs) {\n      var urls = ['https://cdn.holoviz.org/panel/0.14.4/dist/bundled/gridstack/gridstack@4.2.5/dist/gridstack-h5.js'];\n      for (var i = 0; i < urls.length; i++) {\n        skip.push(urls[i])\n      }\n    }    if (((window['Notyf'] !== undefined) && (!(window['Notyf'] instanceof HTMLElement))) || window.requirejs) {\n      var urls = ['https://cdn.holoviz.org/panel/0.14.4/dist/bundled/notificationarea/notyf@3/notyf.min.js'];\n      for (var i = 0; i < urls.length; i++) {\n        skip.push(urls[i])\n      }\n    }    for (var i = 0; i < js_urls.length; i++) {\n      var url = js_urls[i];\n      if (skip.indexOf(url) >= 0) {\n\tif (!window.requirejs) {\n\t  on_load();\n\t}\n\tcontinue;\n      }\n      var element = document.createElement('script');\n      element.onload = on_load;\n      element.onerror = on_error;\n      element.async = false;\n      element.src = url;\n      console.debug(\"Bokeh: injecting script tag for BokehJS library: \", url);\n      document.head.appendChild(element);\n    }\n    for (var i = 0; i < js_modules.length; i++) {\n      var url = js_modules[i];\n      if (skip.indexOf(url) >= 0) {\n\tif (!window.requirejs) {\n\t  on_load();\n\t}\n\tcontinue;\n      }\n      var element = document.createElement('script');\n      element.onload = on_load;\n      element.onerror = on_error;\n      element.async = false;\n      element.src = url;\n      element.type = \"module\";\n      console.debug(\"Bokeh: injecting script tag for BokehJS library: \", url);\n      document.head.appendChild(element);\n    }\n    if (!js_urls.length && !js_modules.length) {\n      on_load()\n    }\n  };\n\n  function inject_raw_css(css) {\n    const element = document.createElement(\"style\");\n    element.appendChild(document.createTextNode(css));\n    document.body.appendChild(element);\n  }\n\n  var js_urls = [\"https://cdn.bokeh.org/bokeh/release/bokeh-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-gl-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-widgets-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.4.3.min.js\", \"https://cdn.bokeh.org/bokeh/release/bokeh-mathjax-2.4.3.min.js\", \"https://unpkg.com/@holoviz/panel@0.14.4/dist/panel.min.js\"];\n  var js_modules = [];\n  var css_urls = [\"https://cdn.holoviz.org/panel/0.14.4/dist/css/widgets.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/loading.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/alerts.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/debugger.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/json.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/card.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/dataframe.css\", \"https://cdn.holoviz.org/panel/0.14.4/dist/css/markdown.css\"];\n  var inline_js = [    function(Bokeh) {\n      inject_raw_css(\"\\n    .bk.pn-loading.arc:before {\\n      background-image: url(\\\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\\\");\\n      background-size: auto calc(min(50%, 400px));\\n    }\\n    \");\n    },    function(Bokeh) {\n      Bokeh.set_log_level(\"info\");\n    },\nfunction(Bokeh) {} // ensure no trailing comma for IE\n  ];\n\n  function run_inline_js() {\n    if ((root.Bokeh !== undefined) || (force === true)) {\n      for (var i = 0; i < inline_js.length; i++) {\n        inline_js[i].call(root, root.Bokeh);\n      }} else if (Date.now() < root._bokeh_timeout) {\n      setTimeout(run_inline_js, 100);\n    } else if (!root._bokeh_failed_load) {\n      console.log(\"Bokeh: BokehJS failed to load within specified timeout.\");\n      root._bokeh_failed_load = true;\n    }\n  }\n\n  if (root._bokeh_is_loading === 0) {\n    console.debug(\"Bokeh: BokehJS loaded, going straight to plotting\");\n    run_inline_js();\n  } else {\n    load_libs(css_urls, js_urls, js_modules, function() {\n      console.debug(\"Bokeh: BokehJS plotting callback run at\", now());\n      run_inline_js();\n    });\n  }\n}(window));",
            "application/vnd.holoviews_load.v0+json": ""
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {
            "application/javascript": "\nif ((window.PyViz === undefined) || (window.PyViz instanceof HTMLElement)) {\n  window.PyViz = {comms: {}, comm_status:{}, kernels:{}, receivers: {}, plot_index: []}\n}\n\n\n    function JupyterCommManager() {\n    }\n\n    JupyterCommManager.prototype.register_target = function(plot_id, comm_id, msg_handler) {\n      if (window.comm_manager || ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null))) {\n        var comm_manager = window.comm_manager || Jupyter.notebook.kernel.comm_manager;\n        comm_manager.register_target(comm_id, function(comm) {\n          comm.on_msg(msg_handler);\n        });\n      } else if ((plot_id in window.PyViz.kernels) && (window.PyViz.kernels[plot_id])) {\n        window.PyViz.kernels[plot_id].registerCommTarget(comm_id, function(comm) {\n          comm.onMsg = msg_handler;\n        });\n      } else if (typeof google != 'undefined' && google.colab.kernel != null) {\n        google.colab.kernel.comms.registerTarget(comm_id, (comm) => {\n          var messages = comm.messages[Symbol.asyncIterator]();\n          function processIteratorResult(result) {\n            var message = result.value;\n            console.log(message)\n            var content = {data: message.data, comm_id};\n            var buffers = []\n            for (var buffer of message.buffers || []) {\n              buffers.push(new DataView(buffer))\n            }\n            var metadata = message.metadata || {};\n            var msg = {content, buffers, metadata}\n            msg_handler(msg);\n            return messages.next().then(processIteratorResult);\n          }\n          return messages.next().then(processIteratorResult);\n        })\n      }\n    }\n\n    JupyterCommManager.prototype.get_client_comm = function(plot_id, comm_id, msg_handler) {\n      if (comm_id in window.PyViz.comms) {\n        return window.PyViz.comms[comm_id];\n      } else if (window.comm_manager || ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null))) {\n        var comm_manager = window.comm_manager || Jupyter.notebook.kernel.comm_manager;\n        var comm = comm_manager.new_comm(comm_id, {}, {}, {}, comm_id);\n        if (msg_handler) {\n          comm.on_msg(msg_handler);\n        }\n      } else if ((plot_id in window.PyViz.kernels) && (window.PyViz.kernels[plot_id])) {\n        var comm = window.PyViz.kernels[plot_id].connectToComm(comm_id);\n        comm.open();\n        if (msg_handler) {\n          comm.onMsg = msg_handler;\n        }\n      } else if (typeof google != 'undefined' && google.colab.kernel != null) {\n        var comm_promise = google.colab.kernel.comms.open(comm_id)\n        comm_promise.then((comm) => {\n          window.PyViz.comms[comm_id] = comm;\n          if (msg_handler) {\n            var messages = comm.messages[Symbol.asyncIterator]();\n            function processIteratorResult(result) {\n              var message = result.value;\n              var content = {data: message.data};\n              var metadata = message.metadata || {comm_id};\n              var msg = {content, metadata}\n              msg_handler(msg);\n              return messages.next().then(processIteratorResult);\n            }\n            return messages.next().then(processIteratorResult);\n          }\n        }) \n        var sendClosure = (data, metadata, buffers, disposeOnDone) => {\n          return comm_promise.then((comm) => {\n            comm.send(data, metadata, buffers, disposeOnDone);\n          });\n        };\n        var comm = {\n          send: sendClosure\n        };\n      }\n      window.PyViz.comms[comm_id] = comm;\n      return comm;\n    }\n    window.PyViz.comm_manager = new JupyterCommManager();\n    \n\n\nvar JS_MIME_TYPE = 'application/javascript';\nvar HTML_MIME_TYPE = 'text/html';\nvar EXEC_MIME_TYPE = 'application/vnd.holoviews_exec.v0+json';\nvar CLASS_NAME = 'output';\n\n/**\n * Render data to the DOM node\n */\nfunction render(props, node) {\n  var div = document.createElement(\"div\");\n  var script = document.createElement(\"script\");\n  node.appendChild(div);\n  node.appendChild(script);\n}\n\n/**\n * Handle when a new output is added\n */\nfunction handle_add_output(event, handle) {\n  var output_area = handle.output_area;\n  var output = handle.output;\n  if ((output.data == undefined) || (!output.data.hasOwnProperty(EXEC_MIME_TYPE))) {\n    return\n  }\n  var id = output.metadata[EXEC_MIME_TYPE][\"id\"];\n  var toinsert = output_area.element.find(\".\" + CLASS_NAME.split(' ')[0]);\n  if (id !== undefined) {\n    var nchildren = toinsert.length;\n    var html_node = toinsert[nchildren-1].children[0];\n    html_node.innerHTML = output.data[HTML_MIME_TYPE];\n    var scripts = [];\n    var nodelist = html_node.querySelectorAll(\"script\");\n    for (var i in nodelist) {\n      if (nodelist.hasOwnProperty(i)) {\n        scripts.push(nodelist[i])\n      }\n    }\n\n    scripts.forEach( function (oldScript) {\n      var newScript = document.createElement(\"script\");\n      var attrs = [];\n      var nodemap = oldScript.attributes;\n      for (var j in nodemap) {\n        if (nodemap.hasOwnProperty(j)) {\n          attrs.push(nodemap[j])\n        }\n      }\n      attrs.forEach(function(attr) { newScript.setAttribute(attr.name, attr.value) });\n      newScript.appendChild(document.createTextNode(oldScript.innerHTML));\n      oldScript.parentNode.replaceChild(newScript, oldScript);\n    });\n    if (JS_MIME_TYPE in output.data) {\n      toinsert[nchildren-1].children[1].textContent = output.data[JS_MIME_TYPE];\n    }\n    output_area._hv_plot_id = id;\n    if ((window.Bokeh !== undefined) && (id in Bokeh.index)) {\n      window.PyViz.plot_index[id] = Bokeh.index[id];\n    } else {\n      window.PyViz.plot_index[id] = null;\n    }\n  } else if (output.metadata[EXEC_MIME_TYPE][\"server_id\"] !== undefined) {\n    var bk_div = document.createElement(\"div\");\n    bk_div.innerHTML = output.data[HTML_MIME_TYPE];\n    var script_attrs = bk_div.children[0].attributes;\n    for (var i = 0; i < script_attrs.length; i++) {\n      toinsert[toinsert.length - 1].childNodes[1].setAttribute(script_attrs[i].name, script_attrs[i].value);\n    }\n    // store reference to server id on output_area\n    output_area._bokeh_server_id = output.metadata[EXEC_MIME_TYPE][\"server_id\"];\n  }\n}\n\n/**\n * Handle when an output is cleared or removed\n */\nfunction handle_clear_output(event, handle) {\n  var id = handle.cell.output_area._hv_plot_id;\n  var server_id = handle.cell.output_area._bokeh_server_id;\n  if (((id === undefined) || !(id in PyViz.plot_index)) && (server_id !== undefined)) { return; }\n  var comm = window.PyViz.comm_manager.get_client_comm(\"hv-extension-comm\", \"hv-extension-comm\", function () {});\n  if (server_id !== null) {\n    comm.send({event_type: 'server_delete', 'id': server_id});\n    return;\n  } else if (comm !== null) {\n    comm.send({event_type: 'delete', 'id': id});\n  }\n  delete PyViz.plot_index[id];\n  if ((window.Bokeh !== undefined) & (id in window.Bokeh.index)) {\n    var doc = window.Bokeh.index[id].model.document\n    doc.clear();\n    const i = window.Bokeh.documents.indexOf(doc);\n    if (i > -1) {\n      window.Bokeh.documents.splice(i, 1);\n    }\n  }\n}\n\n/**\n * Handle kernel restart event\n */\nfunction handle_kernel_cleanup(event, handle) {\n  delete PyViz.comms[\"hv-extension-comm\"];\n  window.PyViz.plot_index = {}\n}\n\n/**\n * Handle update_display_data messages\n */\nfunction handle_update_output(event, handle) {\n  handle_clear_output(event, {cell: {output_area: handle.output_area}})\n  handle_add_output(event, handle)\n}\n\nfunction register_renderer(events, OutputArea) {\n  function append_mime(data, metadata, element) {\n    // create a DOM node to render to\n    var toinsert = this.create_output_subarea(\n    metadata,\n    CLASS_NAME,\n    EXEC_MIME_TYPE\n    );\n    this.keyboard_manager.register_events(toinsert);\n    // Render to node\n    var props = {data: data, metadata: metadata[EXEC_MIME_TYPE]};\n    render(props, toinsert[0]);\n    element.append(toinsert);\n    return toinsert\n  }\n\n  events.on('output_added.OutputArea', handle_add_output);\n  events.on('output_updated.OutputArea', handle_update_output);\n  events.on('clear_output.CodeCell', handle_clear_output);\n  events.on('delete.Cell', handle_clear_output);\n  events.on('kernel_ready.Kernel', handle_kernel_cleanup);\n\n  OutputArea.prototype.register_mime_type(EXEC_MIME_TYPE, append_mime, {\n    safe: true,\n    index: 0\n  });\n}\n\nif (window.Jupyter !== undefined) {\n  try {\n    var events = require('base/js/events');\n    var OutputArea = require('notebook/js/outputarea').OutputArea;\n    if (OutputArea.prototype.mime_types().indexOf(EXEC_MIME_TYPE) == -1) {\n      register_renderer(events, OutputArea);\n    }\n  } catch(err) {\n  }\n}\n",
            "application/vnd.holoviews_load.v0+json": ""
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {
            "text/html": [
              "<style>.bk-root, .bk-root .bk:before, .bk-root .bk:after {\n",
              "  font-family: var(--jp-ui-font-size1);\n",
              "  font-size: var(--jp-ui-font-size1);\n",
              "  color: var(--jp-ui-font-color1);\n",
              "}\n",
              "</style>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {},
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "data": {
            "application/vnd.holoviews_exec.v0+json": "",
            "text/html": [
              "<div id='1047'>\n",
              "  <div class=\"bk-root\" id=\"962c5c8b-a5c5-4f76-9037-a8a979c3e256\" data-root-id=\"1047\"></div>\n",
              "</div>\n",
              "<script type=\"application/javascript\">(function(root) {\n",
              "  function embed_document(root) {\n",
              "    var docs_json = {\"2fff2bf1-4fa3-476f-b465-d7b4e19eae71\":{\"defs\":[{\"extends\":null,\"module\":null,\"name\":\"ReactiveHTML1\",\"overrides\":[],\"properties\":[]},{\"extends\":null,\"module\":null,\"name\":\"FlexBox1\",\"overrides\":[],\"properties\":[{\"default\":\"flex-start\",\"kind\":null,\"name\":\"align_content\"},{\"default\":\"flex-start\",\"kind\":null,\"name\":\"align_items\"},{\"default\":\"row\",\"kind\":null,\"name\":\"flex_direction\"},{\"default\":\"wrap\",\"kind\":null,\"name\":\"flex_wrap\"},{\"default\":\"flex-start\",\"kind\":null,\"name\":\"justify_content\"}]},{\"extends\":null,\"module\":null,\"name\":\"GridStack1\",\"overrides\":[],\"properties\":[{\"default\":\"warn\",\"kind\":null,\"name\":\"mode\"},{\"default\":null,\"kind\":null,\"name\":\"ncols\"},{\"default\":null,\"kind\":null,\"name\":\"nrows\"},{\"default\":true,\"kind\":null,\"name\":\"allow_resize\"},{\"default\":true,\"kind\":null,\"name\":\"allow_drag\"},{\"default\":[],\"kind\":null,\"name\":\"state\"}]},{\"extends\":null,\"module\":null,\"name\":\"click1\",\"overrides\":[],\"properties\":[{\"default\":\"\",\"kind\":null,\"name\":\"terminal_output\"},{\"default\":\"\",\"kind\":null,\"name\":\"debug_name\"},{\"default\":0,\"kind\":null,\"name\":\"clears\"}]},{\"extends\":null,\"module\":null,\"name\":\"NotificationAreaBase1\",\"overrides\":[],\"properties\":[{\"default\":\"bottom-right\",\"kind\":null,\"name\":\"position\"},{\"default\":0,\"kind\":null,\"name\":\"_clear\"}]},{\"extends\":null,\"module\":null,\"name\":\"NotificationArea1\",\"overrides\":[],\"properties\":[{\"default\":[],\"kind\":null,\"name\":\"notifications\"},{\"default\":\"bottom-right\",\"kind\":null,\"name\":\"position\"},{\"default\":0,\"kind\":null,\"name\":\"_clear\"},{\"default\":[{\"background\":\"#ffc107\",\"icon\":{\"className\":\"fas fa-exclamation-triangle\",\"color\":\"white\",\"tagName\":\"i\"},\"type\":\"warning\"},{\"background\":\"#007bff\",\"icon\":{\"className\":\"fas fa-info-circle\",\"color\":\"white\",\"tagName\":\"i\"},\"type\":\"info\"}],\"kind\":null,\"name\":\"types\"}]},{\"extends\":null,\"module\":null,\"name\":\"Notification\",\"overrides\":[],\"properties\":[{\"default\":null,\"kind\":null,\"name\":\"background\"},{\"default\":3000,\"kind\":null,\"name\":\"duration\"},{\"default\":null,\"kind\":null,\"name\":\"icon\"},{\"default\":\"\",\"kind\":null,\"name\":\"message\"},{\"default\":null,\"kind\":null,\"name\":\"notification_type\"},{\"default\":false,\"kind\":null,\"name\":\"_destroyed\"}]},{\"extends\":null,\"module\":null,\"name\":\"TemplateActions1\",\"overrides\":[],\"properties\":[{\"default\":0,\"kind\":null,\"name\":\"open_modal\"},{\"default\":0,\"kind\":null,\"name\":\"close_modal\"}]},{\"extends\":null,\"module\":null,\"name\":\"MaterialTemplateActions1\",\"overrides\":[],\"properties\":[{\"default\":0,\"kind\":null,\"name\":\"open_modal\"},{\"default\":0,\"kind\":null,\"name\":\"close_modal\"}]}],\"roots\":{\"references\":[{\"attributes\":{\"margin\":[5,10,5,10],\"sizing_mode\":\"fixed\",\"text\":\"&lt;div style=&quot;font-size: 18pt; color: black&quot;&gt;N.06 Telok Ayer Tawar&lt;/div&gt;\\n&lt;div style=&quot;font-size: 54pt; color: black&quot;&gt;-&lt;/div&gt;\"},\"id\":\"1049\",\"type\":\"panel.models.markup.HTML\"},{\"attributes\":{\"children\":[{\"id\":\"1051\"},{\"id\":\"1052\"},{\"id\":\"1053\"}],\"margin\":[0,0,0,0],\"name\":\"Row00174\",\"sizing_mode\":\"stretch_width\"},\"id\":\"1050\",\"type\":\"Row\"},{\"attributes\":{\"children\":[{\"id\":\"1048\"}],\"margin\":[0,0,0,0],\"name\":\"Column00177\",\"sizing_mode\":\"scale_both\"},\"id\":\"1047\",\"type\":\"Column\"},{\"attributes\":{\"margin\":[5,10,5,10],\"sizing_mode\":\"fixed\",\"text\":\"&lt;div style=&quot;font-size: 18pt; color: blue&quot;&gt;Maximum Elevation&lt;/div&gt;\\n&lt;div style=&quot;font-size: 54pt; color: blue&quot;&gt;26.0&lt;/div&gt;\"},\"id\":\"1052\",\"type\":\"panel.models.markup.HTML\"},{\"attributes\":{\"margin\":[5,10,5,10],\"sizing_mode\":\"fixed\",\"text\":\"&lt;div style=&quot;font-size: 18pt; color: black&quot;&gt;Population&lt;/div&gt;\\n&lt;div style=&quot;font-size: 54pt; color: black&quot;&gt;29830&lt;/div&gt;\"},\"id\":\"1051\",\"type\":\"panel.models.markup.HTML\"},{\"attributes\":{\"height\":400,\"margin\":[5,5,5,5],\"name\":\"Folium00168\",\"sizing_mode\":\"stretch_width\",\"text\":\"&lt;div style=&quot;width:100%;height:100%&quot;&gt;&lt;div style=&quot;position:relative;width:100%;height:100%;padding-bottom:0%;&quot;&gt;&lt;span style=&quot;color:#565656&quot;&gt;Make this Notebook Trusted to load map: File -&gt; Trust Notebook&lt;/span&gt;&lt;iframe srcdoc=&quot;&amp;lt;!DOCTYPE html&amp;gt;\\n&amp;lt;html&amp;gt;\\n&amp;lt;head&amp;gt;\\n    \\n    &amp;lt;meta http-equiv=&amp;quot;content-type&amp;quot; content=&amp;quot;text/html; charset=UTF-8&amp;quot; /&amp;gt;\\n    \\n        &amp;lt;script&amp;gt;\\n            L_NO_TOUCH = false;\\n            L_DISABLE_3D = false;\\n        &amp;lt;/script&amp;gt;\\n    \\n    &amp;lt;style&amp;gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&amp;lt;/style&amp;gt;\\n    &amp;lt;style&amp;gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&amp;lt;/style&amp;gt;\\n    &amp;lt;script src=&amp;quot;https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js&amp;quot;&amp;gt;&amp;lt;/script&amp;gt;\\n    &amp;lt;script src=&amp;quot;https://code.jquery.com/jquery-1.12.4.min.js&amp;quot;&amp;gt;&amp;lt;/script&amp;gt;\\n    &amp;lt;script src=&amp;quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js&amp;quot;&amp;gt;&amp;lt;/script&amp;gt;\\n    &amp;lt;script src=&amp;quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&amp;quot;&amp;gt;&amp;lt;/script&amp;gt;\\n    &amp;lt;link rel=&amp;quot;stylesheet&amp;quot; href=&amp;quot;https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css&amp;quot;/&amp;gt;\\n    &amp;lt;link rel=&amp;quot;stylesheet&amp;quot; href=&amp;quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css&amp;quot;/&amp;gt;\\n    &amp;lt;link rel=&amp;quot;stylesheet&amp;quot; href=&amp;quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css&amp;quot;/&amp;gt;\\n    &amp;lt;link rel=&amp;quot;stylesheet&amp;quot; href=&amp;quot;https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css&amp;quot;/&amp;gt;\\n    &amp;lt;link rel=&amp;quot;stylesheet&amp;quot; href=&amp;quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&amp;quot;/&amp;gt;\\n    &amp;lt;link rel=&amp;quot;stylesheet&amp;quot; href=&amp;quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&amp;quot;/&amp;gt;\\n    \\n            &amp;lt;meta name=&amp;quot;viewport&amp;quot; content=&amp;quot;width=device-width,\\n                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&amp;quot; /&amp;gt;\\n            &amp;lt;style&amp;gt;\\n                #map_cb842ed82230c892cc7bfd4d09d6762a {\\n                    position: relative;\\n                    width: 100.0%;\\n                    height: 100.0%;\\n                    left: 0.0%;\\n                    top: 0.0%;\\n                }\\n            &amp;lt;/style&amp;gt;\\n        \\n    \\n                    &amp;lt;style&amp;gt;\\n                        .foliumtooltip {\\n                            \\n                        }\\n                       .foliumtooltip table{\\n                            margin: auto;\\n                        }\\n                        .foliumtooltip tr{\\n                            text-align: left;\\n                        }\\n                        .foliumtooltip th{\\n                            padding: 2px; padding-right: 8px;\\n                        }\\n                    &amp;lt;/style&amp;gt;\\n            \\n&amp;lt;/head&amp;gt;\\n&amp;lt;body&amp;gt;\\n    \\n    \\n            &amp;lt;div class=&amp;quot;folium-map&amp;quot; id=&amp;quot;map_cb842ed82230c892cc7bfd4d09d6762a&amp;quot; &amp;gt;&amp;lt;/div&amp;gt;\\n        \\n&amp;lt;/body&amp;gt;\\n&amp;lt;script&amp;gt;\\n    \\n    \\n            var map_cb842ed82230c892cc7bfd4d09d6762a = L.map(\\n                &amp;quot;map_cb842ed82230c892cc7bfd4d09d6762a&amp;quot;,\\n                {\\n                    center: [5.016806622688496, 107.9456777002687],\\n                    crs: L.CRS.EPSG3857,\\n                    zoom: 6,\\n                    zoomControl: true,\\n                    preferCanvas: false,\\n                }\\n            );\\n\\n            \\n\\n        \\n    \\n            var tile_layer_42afe73e5273b996c8c30beecc998e96 = L.tileLayer(\\n                &amp;quot;https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png&amp;quot;,\\n                {&amp;quot;attribution&amp;quot;: &amp;quot;\\\\u0026copy; \\\\u003ca href=\\\\&amp;quot;http://www.openstreetmap.org/copyright\\\\&amp;quot;\\\\u003eOpenStreetMap\\\\u003c/a\\\\u003e contributors \\\\u0026copy; \\\\u003ca href=\\\\&amp;quot;http://cartodb.com/attributions\\\\&amp;quot;\\\\u003eCartoDB\\\\u003c/a\\\\u003e, CartoDB \\\\u003ca href =\\\\&amp;quot;http://cartodb.com/attributions\\\\&amp;quot;\\\\u003eattributions\\\\u003c/a\\\\u003e&amp;quot;, &amp;quot;detectRetina&amp;quot;: false, &amp;quot;maxNativeZoom&amp;quot;: 18, &amp;quot;maxZoom&amp;quot;: 18, &amp;quot;minZoom&amp;quot;: 0, &amp;quot;noWrap&amp;quot;: false, &amp;quot;opacity&amp;quot;: 1, &amp;quot;subdomains&amp;quot;: &amp;quot;abc&amp;quot;, &amp;quot;tms&amp;quot;: false}\\n            ).addTo(map_cb842ed82230c892cc7bfd4d09d6762a);\\n        \\n    \\n\\n        function geo_json_c5827efec75dfd20013a974b55ac10f9_onEachFeature(feature, layer) {\\n            layer.on({\\n            });\\n        };\\n        var geo_json_c5827efec75dfd20013a974b55ac10f9 = L.geoJson(null, {\\n                onEachFeature: geo_json_c5827efec75dfd20013a974b55ac10f9_onEachFeature,\\n            \\n        });\\n\\n        function geo_json_c5827efec75dfd20013a974b55ac10f9_add (data) {\\n            geo_json_c5827efec75dfd20013a974b55ac10f9\\n                .addData(data)\\n                .addTo(map_cb842ed82230c892cc7bfd4d09d6762a);\\n        }\\n            geo_json_c5827efec75dfd20013a974b55ac10f9_add({&amp;quot;features&amp;quot;: [{&amp;quot;geometry&amp;quot;: {&amp;quot;coordinates&amp;quot;: [[[[100.40367, 5.50249], [100.40469, 5.49831], [100.40792, 5.49689], [100.40764, 5.49423], [100.41375, 5.49298], [100.41469, 5.4859], [100.41866, 5.48445], [100.41887, 5.48288], [100.40564, 5.47446], [100.39467, 5.47253], [100.39737, 5.46132], [100.39913, 5.46026], [100.39888, 5.45676], [100.39382, 5.45608], [100.39328, 5.4524], [100.39014, 5.45173], [100.38971, 5.45046], [100.39402, 5.447], [100.38862, 5.44427], [100.37948, 5.44463], [100.37968, 5.44583], [100.37764, 5.4461], [100.37793, 5.46886], [100.37493, 5.49606], [100.38259, 5.498], [100.38456, 5.49687], [100.39869, 5.50703], [100.40367, 5.50249]]]], &amp;quot;type&amp;quot;: &amp;quot;MultiPolygon&amp;quot;}, &amp;quot;properties&amp;quot;: {&amp;quot;code_dun&amp;quot;: &amp;quot;N.06&amp;quot;, &amp;quot;code_parlimen&amp;quot;: &amp;quot;P.042&amp;quot;, &amp;quot;code_state&amp;quot;: 7, &amp;quot;code_state_dun&amp;quot;: &amp;quot;7_N.06&amp;quot;, &amp;quot;dun&amp;quot;: &amp;quot;N.06 Telok Ayer Tawar&amp;quot;, &amp;quot;parlimen&amp;quot;: &amp;quot;P.042 Tasek Gelugor&amp;quot;, &amp;quot;state&amp;quot;: &amp;quot;Pulau Pinang&amp;quot;}, &amp;quot;type&amp;quot;: &amp;quot;Feature&amp;quot;}], &amp;quot;type&amp;quot;: &amp;quot;FeatureCollection&amp;quot;});\\n\\n        \\n    \\n    geo_json_c5827efec75dfd20013a974b55ac10f9.bindTooltip(\\n    function(layer){\\n    let div = L.DomUtil.create(&amp;#x27;div&amp;#x27;);\\n    \\n    let handleObject = feature=&amp;gt;typeof(feature)==&amp;#x27;object&amp;#x27; ? JSON.stringify(feature) : feature;\\n    let fields = [&amp;quot;dun&amp;quot;, &amp;quot;parlimen&amp;quot;];\\n    let aliases = [&amp;quot;dun&amp;quot;, &amp;quot;parlimen&amp;quot;];\\n    let table = &amp;#x27;&amp;lt;table&amp;gt;&amp;#x27; +\\n        String(\\n        fields.map(\\n        (v,i)=&amp;gt;\\n        `&amp;lt;tr&amp;gt;\\n            &amp;lt;th&amp;gt;${aliases[i]}&amp;lt;/th&amp;gt;\\n            \\n            &amp;lt;td&amp;gt;${handleObject(layer.feature.properties[v])}&amp;lt;/td&amp;gt;\\n        &amp;lt;/tr&amp;gt;`).join(&amp;#x27;&amp;#x27;))\\n    +&amp;#x27;&amp;lt;/table&amp;gt;&amp;#x27;;\\n    div.innerHTML=table;\\n    \\n    return div\\n    }\\n    ,{&amp;quot;className&amp;quot;: &amp;quot;foliumtooltip&amp;quot;, &amp;quot;sticky&amp;quot;: true});\\n                     \\n    \\n            map_cb842ed82230c892cc7bfd4d09d6762a.fitBounds(\\n                [[5.44427, 100.37493], [5.50703, 100.41887]],\\n                {&amp;quot;padding&amp;quot;: [30, 30]}\\n            );\\n        \\n&amp;lt;/script&amp;gt;\\n&amp;lt;/html&amp;gt;&quot; style=&quot;position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;&quot; allowfullscreen webkitallowfullscreen mozallowfullscreen&gt;&lt;/iframe&gt;&lt;/div&gt;&lt;/div&gt;\"},\"id\":\"1054\",\"type\":\"panel.models.markup.HTML\"},{\"attributes\":{\"margin\":[5,10,5,10],\"sizing_mode\":\"fixed\",\"text\":\"&lt;div style=&quot;font-size: 18pt; color: red&quot;&gt;Surface covered in water&lt;/div&gt;\\n&lt;div style=&quot;font-size: 54pt; color: red&quot;&gt;0.897&lt;/div&gt;\"},\"id\":\"1053\",\"type\":\"panel.models.markup.HTML\"},{\"attributes\":{\"children\":[{\"id\":\"1049\"},{\"id\":\"1050\"},{\"id\":\"1054\"}],\"margin\":[0,0,0,0],\"name\":\"Column00176\",\"sizing_mode\":\"scale_both\"},\"id\":\"1048\",\"type\":\"Column\"},{\"attributes\":{\"client_comm_id\":\"6926a6073c4f46b7842a5e5724976d38\",\"comm_id\":\"557fd0cbe11841d78ae2d8899501a10d\",\"plot_id\":\"1047\"},\"id\":\"1055\",\"type\":\"panel.models.comm_manager.CommManager\"}],\"root_ids\":[\"1047\",\"1055\"]},\"title\":\"Bokeh Application\",\"version\":\"2.4.3\"}};\n",
              "    var render_items = [{\"docid\":\"2fff2bf1-4fa3-476f-b465-d7b4e19eae71\",\"root_ids\":[\"1047\"],\"roots\":{\"1047\":\"962c5c8b-a5c5-4f76-9037-a8a979c3e256\"}}];\n",
              "    root.Bokeh.embed.embed_items_notebook(docs_json, render_items);\n",
              "    for (const render_item of render_items) {\n",
              "      for (const root_id of render_item.root_ids) {\n",
              "\tconst id_el = document.getElementById(root_id)\n",
              "\tif (id_el.children.length && (id_el.children[0].className === 'bk-root')) {\n",
              "\t  const root_el = id_el.children[0]\n",
              "\t  root_el.id = root_el.id + '-rendered'\n",
              "\t}\n",
              "      }\n",
              "    }\n",
              "  }\n",
              "  if (root.Bokeh !== undefined && root.Bokeh.Panel !== undefined) {\n",
              "    embed_document(root);\n",
              "  } else {\n",
              "    var attempts = 0;\n",
              "    var timer = setInterval(function(root) {\n",
              "      if (root.Bokeh !== undefined && root.Bokeh.Panel !== undefined) {\n",
              "        clearInterval(timer);\n",
              "        embed_document(root);\n",
              "      } else if (document.readyState == \"complete\") {\n",
              "        attempts++;\n",
              "        if (attempts > 200) {\n",
              "          clearInterval(timer);\n",
              "          console.log(\"Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing\");\n",
              "        }\n",
              "      }\n",
              "    }, 25, root)\n",
              "  }\n",
              "})(window);</script>"
            ],
            "text/plain": [
              "Column(sizing_mode='scale_both')\n",
              "    [0] Column(sizing_mode='scale_both')\n",
              "        [0] Number(name='N.06 Telok Ayer Tawar')\n",
              "        [1] Row(sizing_mode='stretch_width')\n",
              "            [0] Number(colors=[(33, 'black')], name='Population', value=29830)\n",
              "            [1] Number(colors=[(66, 'blue')], name='Maximum Elevation', value=26.0)\n",
              "            [2] Number(colors=[(100, 'red')], name='Surface covered i..., value=0.897)\n",
              "        [2] Folium(Map, height=400)"
            ]
          },
          "execution_count": 34,
          "metadata": {
            "application/vnd.holoviews_exec.v0+json": {
              "id": "1047"
            }
          },
          "output_type": "execute_result"
        }
      ],
      "source": [
        "app2 = create_app2(sociodemo, geo_json, select)\n",
        "app2"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "cR5ciqQA1Ye5",
      "metadata": {
        "id": "cR5ciqQA1Ye5"
      },
      "outputs": [],
      "source": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.10.10"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
