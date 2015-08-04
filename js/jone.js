#!/usr/bin/env node

say = function (s) { console.log(s) }
pow = Math.pow
/*
var program = require('jone');

#program
 #   .version('0.0.1')
  #  .usage('<keywords>')
   # .parse(process.argv);

#if(!program.args.length) {
 #   program.help();
#} else {
 #   console.log('Keywords: ' + program.args);   
#}
*/
var empty_object = {};

var stooge = {
    "first-name": "Jerome",
    "last-name": "Howard1"
};
var flight = {
    airline: "Oceanic",
    number: 815,
    departure: {
        IATA: "SYD",
        time: "2004-09-22 14:55",
        city: "Sydney"
    },
    arrival: {
        IATA: "LAX",
        time: "2004-09-23 10:42",
        city: "Los Angeles"
    }
};
var a = {}, b = {}, c = {};
    // a, b, and c each refer to a
    // different empty object
a = b = c = {};
    // a, b, and c all refer to
// the same empty object

c.fred = 100
//console.log(a.fred)

if (typeof Object.create !== 'function') {
     Object.create = function (o) {
         var F = function () {};
         F.prototype = o;
         return new F();
     };
}
var another_stooge = Object.create(stooge);



for (var name in flight) {
    if (typeof flight[name] !== 'function') {
        //console.log(name + ':: ' + flight[name]);
    } 
}

var myObject1 = {
    value: 10,
    increment: function (inc,a) {
	a = a || 1
	inc = typeof inc == 'number' ? inc : 1
//	say({'a':a,'inc': inc,'r':pow(inc,a)})
        this.value += pow(inc,a)
    }
};
myObject1.increment(200,2);
//say(myObject.value);    // 1

//say(10^2)

var myObject = {
    value: 10
}

myObject.double = function (  ) {
    var that = this;    // Workaround.

    var helper = function (  ) {
        that.value = that.value + that.value;
    }; 

    helper(  );    // Invoke helper as a function.
};

// Invoke double as a method.

myObject.double(  );
say(myObject.value);     // 6 


// Create a constructor function called Quo.
// It makes an object with a status property.

var Quo = function (string) {
    this.status = string;
};

// Give all instances of Quo a public method
// called get_status.

Quo.prototype.get_status = function (  ) {
    return this.status;
};

// Make an instance of Quo.

var myQuo = new Quo("confused");

myQuo.status="sadas"

say(myQuo.get_status());  // confused

var x={aas:199,basdsa:2}

Function.prototype.method = function (name, func) {
    if (this.prototype[name]) {
	throw {
	    name: 'OverwriteError',
	    message: 'user function overriding built-in: '+name }}
    this.prototype[name] = func
    return this
}



say(x["aas"])

String.method('trimm', function (  ) {
    return this.replace(/^\s+|\s+$/g, '');
});

say("[" + "  dasdsa   ".trimm( ) + "]")

var factorial = function factorial(i, a) {
    a = a || 1;
    if (i < 2) {
        return a;
    }
    return factorial(i - 1, a * i);
};

say(factorial(100));    // 24

var oo = (function () {
  var z = 0;
  return {
    inc: function (inc) { inc = inc || 1; z += inc},
    get: function ()    { return z }
  }}());

var x=oo
x.inc()
x.inc(120)
say(oo.get())
 
