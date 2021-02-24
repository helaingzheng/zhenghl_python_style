Python语言规范
================================
导入
--------------------

.. tip::
    仅对包和模块使用导入,而不单独导入函数或者类。typing模块例外

定义:
    模块间共享代码的重用机制.
    
优点:
    命名空间管理约定十分简单. 每个标识符的源都用一种一致的方式指示. x.Obj表示Obj对象定义在模块x中.
    
缺点:
    模块名仍可能冲突. 有些模块名太长, 不太方便.
    
结论:
    #. 使用 ``import x`` 来导入包和模块. 
    
    #. 使用 ``from x import y`` , 其中x是包前缀, y是不带前缀的模块名.
    
    #. 使用 ``from x import y as z``, 如果两个要导入的模块都叫做y或者y太长了.
    
    #. 仅当缩写 ``z`` 是通用缩写时才可使用 ``import y as z``.(比如 ``np`` 代表 ``numpy``.)
    
    例如, 模块 ``sound.effects.echo`` 可以用如下方式导入:
    
    .. code-block:: python
    
        from sound.effects import echo
        ...
        echo.EchoFilter(input, output, delay=0.7, atten=4)
     
    导入时不要使用相对名称. 即使模块在同一个包中, 也要使用完整包名. 这能帮助你避免无意间导入一个包两次. 

    导入 ``typing`` 和 `six.moves <https://six.readthedocs.io/#module-six.moves>`_ 模块时可以例外.
    
包
--------------------

.. tip::
    使用模块的全路径名来导入每个模块    

优点:
    避免模块名冲突或是因非预期的模块搜索路径导致导入错误. 查找包更容易. 
    
缺点:
    部署代码变难, 因为你必须复制包层次. 
    
结论:
    所有的新代码都应该用完整包名来导入每个模块.
    
    应该像下面这样导入:  

    yes:
    
    .. code-block:: python
    
        # 在代码中引用完整名称 absl.flags (详细情况).
        import absl.flags
        from doctor.who import jodie

        FLAGS = absl.flags.FLAGS

    .. code-block:: python

        # 在代码中仅引用模块名 flags (常见情况).
        from absl import flags
        from doctor.who import jodie

        FLAGS = flags.FLAGS

    No: (假设当前文件和 `jodie.py` 都在目录 `doctor/who/` 下)

    .. code-block:: python
    
        # 没能清晰指示出作者想要导入的模块和最终被导入的模块.
        # 实际导入的模块将取决于 sys.path.
        import jodie

    不应假定主入口脚本所在的目录就在 `sys.path` 中，虽然这种情况是存在的。当主入口脚本所在目录不在 `sys.path` 中时，代码将假设 `import jodie` 是导入的一个第三方库或者是一个名为 `jodie` 的顶层包，而不是本地的 `jodie.py`


异常
--------------------

.. tip::
    允许使用异常, 但必须小心
 
定义:
    异常是一种跳出代码块的正常控制流来处理错误或者其它异常条件的方式. 
    
优点:
    正常操作代码的控制流不会和错误处理代码混在一起. 当某种条件发生时, 它也允许控制流跳过多个框架. 例如, 一步跳出N个嵌套的函数, 而不必继续执行错误的代码. 
    
缺点:
    可能会导致让人困惑的控制流. 调用库时容易错过错误情况. 
    
结论:
    异常必须遵守特定条件:
    
    #. 优先合理的使用内置异常类.比如 ``ValueError`` 指示了一个程序错误, 比如在方法需要正数的情况下传递了一个负数错误.不要使用 ``assert`` 语句来验证公共API的参数值. ``assert`` 是用来保证内部正确性的,而不是用来强制纠正参数使用.若需要使用异常来指示某些意外情况,不要用 ``assert``,用 ``raise`` 语句,例如:
        
    Yes:
    
    .. code-block:: python

        def connect_to_next_port(self, minimum):
            """Connects to the next available port.

            Args:
                minimum: A port value greater or equal to 1024.

            Returns:
                The new minimum port.

            Raises:
                ConnectionError: If no available port is found.
            """
            if minimum < 1024:
                # Note that this raising of ValueError is not mentioned in the doc
                # string's "Raises:" section because it is not appropriate to
                # guarantee this specific behavioral reaction to API misuse.
                raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
            port = self._find_next_open_port(minimum)
            if not port:
                raise ConnectionError(
                    f'Could not connect to service on port {minimum} or higher.')
            assert port >= minimum, (
                f'Unexpected port {port} when minimum was {minimum}.')
            return port

    No:

    .. code-block:: python

        def connect_to_next_port(self, minimum):
            """Connects to the next available port.

            Args:
            minimum: A port value greater or equal to 1024.

            Returns:
            The new minimum port.
            """
            assert minimum >= 1024, 'Minimum port must be at least 1024.'
            port = self._find_next_open_port(minimum)
            assert port is not None
            return port

    #. 模块或包应该定义自己的特定域的异常基类, 这个基类应该从内建的Exception类继承. 模块的异常基类后缀应该叫做 ``Error``.
    #. 永远不要使用 ``except:`` 语句来捕获所有异常, 也不要捕获 ``Exception`` 或者 ``StandardError`` , 除非你打算重新触发该异常, 或者你已经在当前线程的最外层(记得还是要打印一条错误消息). 在异常这方面, Python非常宽容, ``except:`` 真的会捕获包括Python语法错误在内的任何错误. 使用 ``except:`` 很容易隐藏真正的bug. 
    #. 尽量减少try/except块中的代码量. try块的体积越大, 期望之外的异常就越容易被触发. 这种情况下, try/except块将隐藏真正的错误. 
    #. 使用finally子句来执行那些无论try块中有没有异常都应该被执行的代码. 这对于清理资源常常很有用, 例如关闭文件.

全局变量
--------------------

.. tip::
    避免全局变量

定义:
    定义在模块级的变量.
    
优点:
    偶尔有用. 
    
缺点:
    导入时可能改变模块行为, 因为导入模块时会对模块级变量赋值. 
    
结论:
    避免使用全局变量.
    鼓励使用模块级的常量,例如 ``MAX_HOLY_HANDGRENADE_COUNT = 3``.注意常量命名必须全部大写,用 ``_`` 分隔.具体参见 `命名规则 <https://google.github.io/styleguide/pyguide.html#s3.16-naming>`_
    若必须要使用全局变量,应在模块内声明全局变量,并在名称前 ``_`` 使之成为模块内部变量.外部访问必须通过模块级的公共函数.

推导式&生成式
--------------------------------

.. tip::
    可以在简单情况下使用    

定义:
    列表,字典和集合的推导&生成式提供了一种简洁高效的方式来创建容器和迭代器, 而不必借助map(), filter(), 或者lambda.(译者注: 元组是没有推导式的, ``()`` 内加类似推导式的句式返回的是个生成器)
    
优点:
    简单的列表推导可以比其它的列表创建方法更加清晰简单. 生成器表达式可以十分高效, 因为它们避免了创建整个列表. 
    
缺点:
    复杂的列表推导或者生成器表达式可能难以阅读. 
    
结论:
    适用于简单情况. 每个部分应该单独置于一行: 映射表达式, for语句, 过滤器表达式. 禁止多重for语句或过滤器表达式. 复杂情况下还是使用循环.
    
    Yes:

    .. code-block:: python 

        result = [mapping_expr for value in iterable if filter_expr]

        result = [{'key': value} for value in iterable
                    if a_long_filter_expression(value)]

        result = [complicated_transform(x)
                    for x in iterable if predicate(x)]

        descriptive_name = [
            transform({'key': key, 'value': value}, color='black')
            for key, value in generate_iterable(some_input)
            if complicated_condition_is_met(key, value)
        ]

        result = []
        for x in range(10):
            for y in range(5):
                if x * y > 10:
                    result.append((x, y))

        return {x: complicated_transform(x)
                for x in long_generator_function(parameter)
                if x is not None}

        squares_generator = (x**2 for x in range(10))

        unique_names = {user.name for user in users if user is not None}

        eat(jelly_bean for jelly_bean in jelly_beans
            if jelly_bean.color == 'black')    
              
    No:

    .. code-block:: python 
    
          result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

          return ((x, y, z)
                  for x in xrange(5)
                  for y in xrange(5)
                  if x != y
                  for z in xrange(5)
                  if y != z)

Lambda函数
--------------------

.. tip::
    适用于单行函数

定义:
    与语句相反, lambda在一个表达式中定义匿名函数. 常用于为 ``map()`` 和 ``filter()`` 之类的高阶函数定义回调函数或者操作符.
    
优点:
    方便.
    
缺点:
    比本地函数更难阅读和调试. 没有函数名意味着堆栈跟踪更难理解. 由于lambda函数通常只包含一个表达式, 因此其表达能力有限. 
    
结论:
    适用于单行函数. 如果代码超过60-80个字符, 最好还是定义成常规(嵌套)函数.
    
    对于常见的操作符，例如乘法操作符，使用 ``operator`` 模块中的函数以代替lambda函数. 例如, 推荐使用 ``operator.mul`` , 而不是 ``lambda x, y: x * y`` . 

默认参数值
--------------------

.. tip::
    适用于大部分情况.
    
定义:
    你可以在函数参数列表的最后指定变量的值, 例如, ``def foo(a, b = 0):`` . 如果调用foo时只带一个参数, 则b被设为0. 如果带两个参数, 则b的值等于第二个参数. 
    
优点:
    你经常会碰到一些使用大量默认值的函数, 但偶尔(比较少见)你想要覆盖这些默认值. 默认参数值提供了一种简单的方法来完成这件事, 你不需要为这些罕见的例外定义大量函数. 同时, Python也不支持重载方法和函数, 默认参数是一种"仿造"重载行为的简单方式. 
    
缺点:
    默认参数只在模块加载时求值一次. 如果参数是列表或字典之类的可变类型, 这可能会导致问题. 如果函数修改了对象(例如向列表追加项), 默认值就被修改了. 
    
结论:
    鼓励使用, 不过有如下注意事项:
    
    不要在函数或方法定义中使用可变对象作为默认值.
    
    .. code-block:: python
    
        Yes: def foo(a, b=None):
                if b is None:
                    b = []
        Yes: def foo(a, b: Optional[Sequence] = None):
                if b is None:
                    b = []
        Yes: def foo(a, b: Sequence = ()):  # Empty tuple OK since tuples are immutable 

    .. code-block:: python  

        No:  def foo(a, b=[]):
            ...
        No:  def foo(a, b=time.time()):  # The time the module was loaded???
            ...
        No:  def foo(a, b=FLAGS.my_thing):  # sys.argv has not yet been parsed...
            ...
        No:  def foo(a, b: Mapping = {}):  # Could still get passed to unchecked code             
            ...

True/False的求值
--------------------

.. tip::
    尽可能使用隐式false
    
定义:
    Python在布尔上下文中会将某些值求值为false. 按简单的直觉来讲, 就是所有的"空"值都被认为是false. 因此0， None, [], {}, "" 都被认为是false.
    
优点:
    使用Python布尔值的条件语句更易读也更不易犯错. 大部分情况下, 也更快. 
    
缺点:
    对C/C++开发人员来说, 可能看起来有点怪. 
    
结论:
    尽可能使用隐式的false, 例如: 使用 ``if foo:`` 而不是 ``if foo != []:`` . 不过还是有一些注意事项需要你铭记在心:
    
    #. 对于 ``None`` 等单例对象测试时,使用 ``is`` 或者 ``is not``.当你要测试一个默认值是None的变量或参数是否被设为其它值. 这个值在布尔语义下可能是false!
           (译者注: ``is`` 比较的是对象的id(), 这个函数返回的通常是对象的内存地址,考虑到CPython的对象重用机制,可能会出现生命周不重叠的两个对象会有相同的id)
    #. 永远不要用==将一个布尔量与false相比较. 使用 ``if not x:`` 代替. 如果你需要区分false和None, 你应该用像 ``if not x and x is not None:`` 这样的语句.
    #. 对于序列(字符串, 列表, 元组), 要注意空序列是false. 因此 ``if not seq:`` 或者 ``if seq:`` 比 ``if len(seq):`` 或 ``if not len(seq):`` 要更好.
    #. 处理整数时, 使用隐式false可能会得不偿失(即不小心将None当做0来处理). 你可以将一个已知是整型(且不是len()的返回结果)的值与0比较. 
    
        Yes: 

        .. code-block:: python
        
            if not users:
                print('no users')

            if foo == 0:
                self.handle_zero()

            if i % 10 == 0:
                self.handle_multiple_of_ten()

            def f(x=None):
                if x is None:
                    x = []

        No:

        .. code-block:: python
        
            if len(users) == 0:
                print 'no users'

            if foo is not None and not foo:
                self.handle_zero()

            if not i % 10:
                self.handle_multiple_of_ten()  

            def f(x=None):
                x = x or []
                     
    #. 注意'0'(字符串)会被当做true.


