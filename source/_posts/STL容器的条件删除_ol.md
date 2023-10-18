---
title: STL容器的条件删除
categories: 笔记
tags:
  - C++
date: 2023-10-18 21:28:22
---
# STL容器的条件删除

条件删除非常常见的业务需求，比如删除一些无效或者过期的的数据。但在C++中写出正确且高效的条件删除方法，是需要对STL容器有比较清晰的了解的，也是一个C++程序员基本的素质。

## vetor

从最常用的顺序容器开始。最朴素的想法是从头遍历一次，找到符合条件的，调用`erase`删除。这种方法的复杂度是$O(n^2)$的，因为每删除一次元素，后面的元素都要全部向前移动一位。

C++98代码如下所示：

```c++
// 使用迭代器遍历vector，并删除满足条件的元素
    std::vector<int>::iterator it = v.begin();
    while (it != v.end()) {
        if (pred(*it) {
            it = v.erase(it); // 删除元素并返回下一个元素的迭代器
        } else {
            ++it; // 移动到下一个元素
        }
    }
```

`pred()`代表我们的判断条件，返回值为真则删除。

你或许知道STL中有`remove()`这个函数，不过注意，`remove()`并不真的删除元素，而是把不需要删除的元素放到前面，返回保留元素末尾的迭代器。复杂度是$O(n)$，一趟就可以完成这样的工作。

> 如果不太明白的话可以看下面来自Effective STL的例子（虽然我觉得直接看源码更直观，这么解释反而绕了）：
>
> 我们想要删除容器内值为99的元素。
>
> 调用remove之前v的布局如下：
>
> ![image-20231015214803735](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/STL%E5%AE%B9%E5%99%A8%E7%9A%84%E6%9D%A1%E4%BB%B6%E5%88%A0%E9%99%A4/20231018212813265384_121_image-20231015214803735.png)
>
> 如果我们将remove的返回值保存在一个新的迭代器对象newEnd中，
>
> `vector<int>:iterator newEnd (remove (v.begin ()v.end,99));`
>
> 调用了`remove`之后,`v`的布局应该如下：
>
> 
>
> ![image-20231015214838011](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/STL%E5%AE%B9%E5%99%A8%E7%9A%84%E6%9D%A1%E4%BB%B6%E5%88%A0%E9%99%A4/20231018212816114720_673_image-20231015214838011.png)
>
> remove的行为看起来有点恶意，但它只是算法操作的附带结果。在内部，remove遍历整个区间，用需要保留的元素的值覆盖掉那些要被删除的元素的值。这种覆盖是通过对那些需要被覆盖的元素的赋值来完成的。
>
> 可以把remove想象成一个压缩过程，需要被删除的元素就好像是压缩过程中需要被填充的洞。对于我们的`vector`，其操作过程如下：
>
> 1。`remove`检查`v[0]`，看它的值是否需要被删除，接着看`v[1]`，然后是`v[2]`。
> 2。检查`v[3]`，发现它应该被删除，于是它记住了`v[3]`的值可能要被覆盖。然后移动到`v[4]`上。这就好比注明了`v[3]`是一个需要被填充的“洞”。
> 3。进一步检查`v[4]`，发现它的值需要保留，所以它把`v[4]`赋给`v[3]`，并记住`v[4]`可能需要被覆盖。然后移动到`v[5]`。将`remove`与压缩过程做对比的话，它用`v[4]`填充`v[3]`， 并注明`v[4]`现在是一个洞。
> 4。它发现`v[5]`应该被删除，所以它跳过`v[5]`，移动到`v[6]`。它仍然记住`v[4]`是一个正在等待被填充的洞。
>
> 5。它检查出`v[6]`是一个需要被保留的值，所以它把`v[6]`的值赋给`v[4]`，并记住现在`v[5] `是下一个需要被填充的洞，然后移动到`v[7]`。
>
> 6。它用类似的方式检查`v[7]`、`v[8]`和`v[9]`。它把`v[7]`的值赋给`v[5]`，`v[8]`的值赋给`v[6]`， 忽略`v[9]`，因为`v[9]`的值要被删除。
>
> 7。它返回一个迭代器，指向下一个要被覆盖的元素。对于本例来说，该元素为`v[7]`。
>
> 你可以想象这些值在ⅴ中的移动如下图所示：
>
> ![image-20231015215706746](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/STL%E5%AE%B9%E5%99%A8%E7%9A%84%E6%9D%A1%E4%BB%B6%E5%88%A0%E9%99%A4/20231018212819320796_369_image-20231015215706746.png)
>
> 如果remove所覆盖掉的这些值是指针的话，那么这可能会存在严重的问题（不仅这一点，所有涉及拷贝的算法都是如此。本来用容器存放裸指针就是很坏的决定）。

STL库伪代码如下所示：

```c++
template <class ForwardIterator, class Predicate>
remove_if(ForwardIterator first, ForwardIterator last, Predicate pred)
{
  	//先从第一个需要删除的元素开始查看
    first = std::find_if<ForwardIterator, Predicate&>(first, last, pred);
    if (first != last)
    {
        ForwardIterator i = first;
        while (++i != last)
        {
            if (!pred(*i))
            {
                //把first指针往后看做新的向量，收集不需要删除的元素
                *first = std::move(*i);
                ++first;
            }
        }
    }
    return first;
}
```

上面的代码删除了STL中为隐藏实现细节所做的工作，以便阅读。

然后，我们需要做的就是把后面的元素真正的删除。`erase`可以做到这一点。

因此针对`vector`的最佳实践是：

```c++
v.erase(remove_if(v.begin(), v.end(), pred), v.end());
```

注意到这里用的`remove_if`。它的原理和`remove`相同，`remove`第三个参数是具体值，`remove_if`第三个参数是仿函数（函数对象，lambda等）。

比如删除偶数：

```c++
auto isEven = [](int x) {
        return x % 2 == 0;
    };
v.erase(std::remove_if(v.begin(), v.end(), isEven), v.end());
```

其他顺序容器如`string`，`deque`均可以使用这种方式。

## list

对于list，稍显的有些不同。`list`作为链表，可以高效的进行元素插入删除。我们当然可以用一个循环朴素的删除元素并更新迭代器。

我们知道，如果有STL的成员函数和STL算法，应当优先选择成员函数形式，因为其可以针对特定容器做优化。（Effective STL Item43）

最佳实践是直接调用`list`的成员函数`remove`或`remove_if`：

```c++
l.remove_if(pred);
```

`pred`是仿函数（函数对象，lambda等）

我们来看一下它的实现原理：

```c++
template <class Tp, class Alloc>
template <class Pred>
typename list<Tp, Alloc>::remove_return_type
list<Tp, Alloc>::remove_if(Pred _pred)
{
    list<Tp, Alloc> deleted_nodes(get_allocator()); // collect the nodes we're removing
    for (iterator i = begin(), e = end(); i != e;)
    {
        if (pred(*i))
        {
            iterator j = std::next(i);
            for (; j != e && pred(*j); ++j);
            deleted_nodes.splice(deleted_nodes.end(), *this, i, j);
            i = j;
          	//此时指向的元素若不是end，一定满足！pred(*i)，直接跳过。
            if (i != e)
                ++i;
        }
        else
            ++i;
    }

    return (remove_return_type) deleted_nodes.size();
}
```

同样隐藏了实现细节。可以看到标准库实现对连续存在的待删除元素进行了优化，同时将待删除节点放到临时容器`deleted_nodes`中，返回删除元素数量，并在退出函数作用域后进行析构，释放删除节点的内存。这和智能指针的原理是一样的。

## 关联容器

对于关联容器如`map`，`set`，或者哈希表`unordered_map`等，你可能想，像`vector`一样`remove`然后再`erase`。然后写出了自认为很酷的代码：

```c++
m.erase(std::remove_if(m.begin(), m.end(), [](const auto& pair) {
        return pred(pair.second);
    }), m.end());
```

你会发现编译器报了一长串错误：

```
error occurred here in instantiation of function template specialization 'std::remove_if<std::__map_iterator<std::__tree_iterator<std::__value_type<int, std::string>, std::__tree_node<std::__value_type<int, std::string>, void *> *, long>>, (lambda at /User... copy assignment operator is implicitly deleted because 'pair<const int, std::string>' has a user-declared move constructor
```

从报错原因和`remove_if`STL实现不难看出原因。

我们查看`pair`的源码：

```c++
pair(pair&&) = default;
```

由于使用了移动构造函数（编译器默认生成），拷贝构造函数不会被生成。`remove_if`虽然支持移动语义，但是`map`里面存的是`pair<const int, std::string>`。作为`const`的元素，不能移动无可厚非。拷贝构造函数也没有，那就只好报错了。

所以对于`map`以及其他关联容器的删除，最佳实践只能是遍历然后删除。

```c++
for (auto it = m.begin(); it != m.end(); ) {
    if (it->second.length() == 13) {
        it = m.erase(it);
    } else {
        ++it;
    }
}
```

其他等价的写法也是可以的。

### 统一写法

看到这里，或许会想，真的没有一种统一的方法可以删除容器吗？不同的容器接口还不一样，这心智负担太重了。确实是这样。好的设计应当让接口容易被正确使用，不容易被误用。使用者也不应该依赖其实现。STL虽然很强大，但这一方面STL从一开始并没有做的很好。

不过条件删除这个需求实在是太常见了，因此C++20起，有了新关键字[`erase_if`](https://en.cppreference.com/w/cpp/container/vector/erase2)，为条件删除提供了统一的接口。

其接受两个参数，第一个参数是容器本身，第二个参数是删除的条件。以`set`为例：

```cpp
  std::set data{3, 3, 4, 5, 5, 6, 6, 7, 2, 1, 0};
  auto divisible_by_3 = [](auto const& x) { return (x % 3) == 0; };
  const auto count = std::erase_if(data, divisible_by_3);
```

其等价于：

```cpp
auto old_size = c.size();
for (auto first = c.begin(), last = c.end(); first != last;)
{
    if (pred(*first))
        first = c.erase(first);
    else
        ++first;
}
return old_size - c.size();
```

对于其他容器用法类似。

C++20或许对于实际工程还是有点太新了。我们也可以使用Boost库或者直接在std命名空间添加下面的[代码](https://stackoverflow.com/questions/3424962/where-is-erase-if)（虽然通常不建议修改std命名空间里的东西）：

```cpp
namespace std {

// for std::string
template <class charT, class traits, class A, class Predicate>
void erase_if(basic_string<charT, traits, A>& c, Predicate pred) {
    c.erase(remove_if(c.begin(), c.end(), pred), c.end());
}

// for std::deque
template <class T, class A, class Predicate>
void erase_if(deque<T, A>& c, Predicate pred) {
    c.erase(remove_if(c.begin(), c.end(), pred), c.end());
}

// for std::vector
template <class T, class A, class Predicate>
void erase_if(vector<T, A>& c, Predicate pred) {
    c.erase(remove_if(c.begin(), c.end(), pred), c.end());
}

// for std::list
template <class T, class A, class Predicate>
void erase_if(list<T, A>& c, Predicate pred) {
    c.remove_if(pred);
}

// for std::forward_list
template <class T, class A, class Predicate>
void erase_if(forward_list<T, A>& c, Predicate pred) {
    c.remove_if(pred);
}

// for std::map
template <class K, class T, class C, class A, class Predicate>
void erase_if(map<K, T, C, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

// for std::multimap
template <class K, class T, class C, class A, class Predicate>
void erase_if(multimap<K, T, C, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

// for std::set
template <class K, class C, class A, class Predicate>
void erase_if(set<K, C, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

// for std::multiset
template <class K, class C, class A, class Predicate>
void erase_if(multiset<K, C, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

// for std::unordered_map
template <class K, class T, class H, class P, class A, class Predicate>
void erase_if(unordered_map<K, T, H, P, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

// for std::unordered_multimap
template <class K, class T, class H, class P, class A, class Predicate>
void erase_if(unordered_multimap<K, T, H, P, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

// for std::unordered_set
template <class K, class H, class P, class A, class Predicate>
void erase_if(unordered_set<K, H, P, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

// for std::unordered_multiset
template <class K, class H, class P, class A, class Predicate>
void erase_if(unordered_multiset<K, H, P, A>& c, Predicate pred) {
    for (auto i = c.begin(), last = c.end(); i != last; )
        if (pred(*i))
            i = c.erase(i);
        else
            ++i;
}

} // namespace std
```

可以看到，上面这份代码恰恰是对容器条件删除方式的总结。