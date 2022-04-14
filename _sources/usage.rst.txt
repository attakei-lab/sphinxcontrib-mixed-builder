======
使い方
======

インストール
============

現在はPyPIに登録しておらず、GitHub Releases機能も利用していないため、GitHubリポジトリを直接インストール形式を取る必要があります。

.. code-block:: console

   pip install git+https://github.com/attakei-lab/sphinx-mixed-builder

設定
====

``conf.py`` の ``extensions`` には、 ``sphinxcontrib.mixed_builder`` を追加します。
また、HTMLベースのカスタムビルダーを使う場合は、必要なSphinx拡張も追加します。

.. literalinclude:: conf.py
    :language: python
    :lines: 11-16
    :linenos:

この拡張向けの設定としては、次の2個が存在します。

.. confval:: mixed_builders

    :Type: ``list``
    :Default: ``["html"]``

    この拡張が実際に取り扱うビルダー名をリストで指定します。
    一番最初に指定したビルダーをデフォルトビルダーとして扱い、
    いくつかの処理はデフォルトビルダーのみを使用します。

.. confval:: mixed_rules

    :Type: ``list``
    :Default: ``[]``

    ファイル生成時にどのビルダーを使うかのルールを指定します。

    .. literalinclude:: conf.py
        :language: python
        :lines: 29-34

    リストの各要素が判定ルールとなっており、最初に確定したビルダーを使用します。
    どの判定ルールにも該当しない場合は、デフォルトビルダーを使用します。

    各要素は、次の要素を持ちます。

    - ``builder`` : 使用ビルダー名。Sphinxに登録されており、 ``mixed_builders`` に設定されているものでなければなりません。
    - 他に、ルールに該当するかの判定ように次のいずれかの要素1個（通常はソースファイル名から拡張子を除いたものになります）

      - ``equal`` : 完全一致
      - ``start`` : 前方一致
      - ``end`` : 後方一致

各ビルダー向けの設定を忘れないようにしてください。
