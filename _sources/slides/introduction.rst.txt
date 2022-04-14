====================================================
複数のHTML系ビルダーをまとめて扱う謎ビルダーを作った
====================================================

はじめに
========

お前誰よ
--------

.. figure:: https://attakei.net/_static/images/icon-attakei.jpg

@attakei 

* 趣味系・ライブラリ系Pythonista
* 代表作: ``sphinx-revealjs``


sphinxcontrib-mixed-builder
===========================

なにこれ？
----------

変わり種のSphinx拡張の1つで、

**「複数のビルダーを組み合わせ使う」**

ビルダーを提供します。

どういうこと？
--------------

.. code-block:: text

    - index.rst
    - usage.rst
    - slides/
      - introduce.rst
      - sample-1.rst
      - sample-2.rst

このような構成のSphinxプロジェクト

.. revealjs-break::

.. code-block:: text

    - index.rst       -> html
    - usage.rst       -> html
    - slides/
      - introduce.rst -> html
      - sample-1.rst  -> html
      - sample-2.rst  -> html

``make html`` だと

.. revealjs-break::

.. code-block:: text

    - index.rst       -> revealjs
    - usage.rst       -> revealjs
    - slides/
      - introduce.rst -> revealjs
      - sample-1.rst  -> revealjs
      - sample-2.rst  -> revealjs

``make revealjs`` だと

.. revealjs-break::

.. code-block:: text

    - index.rst       -> html
    - usage.rst       -> html
    - slides/
      - introduce.rst -> revealjs
      - sample-1.rst  -> revealjs
      - sample-2.rst  -> revealjs

``make mixed`` (+適切な設定)なら

.. revealjs-break::

単一ビルドなのに、HTMLとReveal.jsを同居させることが出来る！

使い方
======

PyPI未登録です
--------------

.. code-block:: console

    pip install git+https://github.com/attakei-lab/sphinx-mixed-builder


conf.py
-------

本拡張+他のビルダー拡張を追加する

.. code-block:: python

    extensions = [
        "sphinxcontrib.mixed_builder",
        "sphinx_revealjs",
    ]

.. revealjs-break::

使うビルダー群を指定する

.. code-block:: python

    mixed_builders = ["html", "revealjs"]

.. revealjs-break::

ビルダーの適用ルールを指定する

.. code-block:: python

    mixed_rules = [
        {
            "docname": "slides/introduction",
            "builder": "revealjs",
        }
    ]

ビルドする
----------

``make`` コマンドでビルドしつつ、Pythonのサーバーモジュールで表示確認してみましょう

.. code-block:: console

    make mixed
    python -m http.server -d _build/mixed

おまけ
======

なんでこんなの作ったの？
------------------------

``sphinx-revealjs`` で複数のスライドを管理する際に、「インデックスもReveal.js化する」問題の解消をしたかった。

じゃあ、なんで ``sphinx-revealjs`` に同梱してないの？
-----------------------------------------------------

実装の構想したときに、「これってrevealjsに限らなくね？」って思ったため。

おわり
======
