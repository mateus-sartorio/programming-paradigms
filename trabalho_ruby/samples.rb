# [1, 2, 3, 4].each do |item|
#     p item
# end

# => [1, 2, 3, 4]

# pets = [1, 2, 3, 4]

# puts pets.map { |n| n * 2 }

# => [2, 4, 6, 8]

# foods = { bacon: 'protein', apple: 'fruit' }

# puts foods.map {|k, v| [k, v.upcase]}
# => { bacon: 'PROTEIN', apple: 'FRUIT' }


# puts pets.select { |item| item[:type] == "dog" }

# => {:name=>"Butters", :age=>3, :type=>"dog"}
# => {:name=>"Lizzy", :age=>6, :type=>"dog"}
# => {:name=>"Joey", :age=>3, :type=>"dog"}


# double_it = lambda { |num| num * 2 }
# triple_it = lambda { |num| num * 3 }

# def apply_lambda(lmbda, number)
#     puts lmbda.call(number)
# end

# puts apply_lambda(double_it, 10)
# # => 20

# puts apply_lambda(triple_it, 20)
# # => 60

# def count_by(array, &fn)
#     array.each_with_object(Hash.new(0)) { |v, h|
#         h[fn.call(v)] += 1
#     }
# end

# count_by([1,2,3], &:even?)
# => {false=>2, true=>1}


# def count(array, &fn)
#     array.each_with_object
# end

# puts([1, 2, 3, 4].each_with_object(1) {|v, h|
#     puts v, h, '-'
# })

# def callback
#     puts 'nice bro'
# end

# def f(fn)
#     method(fn).call
# end

# f(:callback)

# def add!(a, b)
#     a + b
# end

# def remove(array,item)
#     array.reject { |v| v == item }

# endarray = [1,2,3]
# remove(array, 1)

# # => [2, 3]

# array
# # => [1, 2, 3]

# def first_option
#     puts "space jam"
# end

# def second_option
#     puts "dogs rule"
# end

# def receives_function(func)
#    method(func).call
# end

# receives_function(:first_option)
# # => space jam

# receives_function(:second_option)
# # => dogs rule

# [1, 2, 3].reduce(0) { |sum, n| sum + n }
# # => 6

# a = 4 + 4i
# puts a

# require 'bigdecimal'

# a = BigDecimal('1.2')
# puts a
# # => 0.12e1

# a = Rational('1/2')
# puts a
# # => 1/2


# a = 1 + 2i
# puts a
# # => 1+2i

# 123456789 ** 2      #=> 15241578750190521
# 123456789 ** 1.2    #=> 5126464716.09932
# 123456789 ** -2     #=> 6.5610001194102e-17

# puts :abc
# # => abc

a = {'first_name': 'Mao', 'last_name': 'Tsé-Tung'}
puts a
# => {:first_name=>"Mao", :last_name=>"Tsé-Tung"}
puts a[:last_name]
# => Tsé-Tung

b = {:first_name => 'Mao', :lat_name => 'Zedong'}
puts b[:first_name]
# => Mao
puts b
# => {:first_name=>"Mao", :second_name=>"Zedong"}


