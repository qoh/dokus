// set set([iterable], [bool allowString])
//
//  A set object is an unordered collection of distinct objects.
//  Common uses include membership testing, removing duplicates from a sequence,
//  and computing mathematical operations such as intersection, union, difference, and symmetric difference.
//
//  This object type is always mutable.
//
//  `set()` creates an empty set, whereas `set(iterable)` creates a set
//  containing unique items from *iterable*.
//
//  Sets are represented as a list of items within braces.
//  Basic example:
//
//      ==>$a = set();
//      ==>$a.add(5);
//      ==>$a.add(9);
//      ==>$a.add("foo");
//      ==>$a.add(4);
//      ==>$a.remove(5);
//      ==>echo(repr($a));
//      {foo, 9, 4}
//      ==>echo(contains($a, 4));
//      1
//
//  @extends ScriptObject
//  @arg iterable A sequence of items to derive from. If not specified, an empty set is created.
//  @arg allowString The `allowString` parameter of `iter(...)`.

function set(%iterable, %allowString)
{
	%obj = new ScriptObject()
	{
		class = set;
	};

	if (%iterable !$= "")
	{
		%iter = iter(%iterable, %allowString);

		if (%iter != 0)
		{
			for (%item = %iter.next(); %iter.next; %item = %iter.next())
			{
				%obj.add(%item);
			}
			
			%iter.delete();
		}
	}

	return %obj;
}

function set::onAdd(%this)
{
	%this.a = 0;
	%this.b = -1;
}

// Operator functions (no, TS doesn't support this, they're separate methods)

function set::__len__(%this)
{
	return (%this.b - %this.a) + 1;
}

function set::__contains__(%this, %item)
{
	return %this.index[%item] !$= "";
}

function set::__iter__(%this, %iter)
{
	%iter._method = "list";
	%iter._max = %this.b - %this.a;

	for (%i = %this.a; %i <= %this.b; %i++)
	{
		%iter._iter[%i - %this.a] = %this.item[%i];
	}
}

function set::__copy__(%this)
{
	return %this.copy();
}

function set::__eq__(%this, %other)
{
	if (%this.b - %this.a != %other.b - %other.a)
	{
		return 0;
	}

	for (%i = %this.a; %i <= %this.b; %i++)
	{
		if (%other.index[%this.item[%i]] $= "")
		{
			return 0;
		}
	}

	return 1;
}

function set::__ne__(%this, %other)
{
	return !%this.__eq__(%other);
}

function set::__lt__(%this, %other)
{
	return %this.__le__(%other) && !%this.__ne__(%other);
}

function set::__gt__(%this, %other)
{
	return %this.__ge__(%other) && !%this.__ne__(%other);
}

function set::__le__(%this, %other)
{
	return %this.issubset(%other);
}

function set::__ge__(%this, %other)
{
	return %this.issuperset(%other);
}

function set::__and__(%this, %other)
{
	return %this.intersection(%other);
}

function set::__or__(%this, %other)
{
	return %this.union(%other);
}

function set::__xor__(%this, %other)
{
	return %this.symmetric_difference(%other);
}

function set::__sub__(%this, %other)
{
	return %this.difference(%other);
}

function set::__bool__(%this, %other)
{
	return %this.b - %this.a > 0;
}

function set::__repr__(%this, %other)
{
	for (%i = %this.a; %i <= %this.b; %i++)
	{
		%str = %str @ repr(%this.item[%i]);

		if (%i != %this.b)
		{
			%str = %str @ ", ";
		}
	}

	return "{" @ %str @ "}";
}

// bool set::add(item)
//  Adds a new item if it is not already contained in the set.
//  Returns whether or not the item was added (was not in the set previously).

function set::add(%this, %item)
{
	if (%this.index[%item] !$= "")
	{
		return 0;
	}

	%index = mAbs(%this.a) < %this.b ? %this.a-- : %this.b++;

	%this.index[%item] = %index;
	%this.item[%index] = %item;

	return 1;
}

// bool set::remove(item)
//  Removes an item if it is contained in the set.
//  Returns whether or not the item was removed (was in the set previously).

function set::remove(%this, %item)
{
	if (%this.index[%item] $= "")
	{
		return 0;
	}

	%a = %this.index[%item] - %this.a;
	%b = %this.b - %this.index[%item];

	%dir = %a < %b ? -1 : 1;
	%end = (%a < %b ? %this.a : %this.b) + %dir;

	for (%i = %this.index[%item]; %i != %dir; %i += %dir)
	{
		%this.item[%i] = %this.item[%i + 1];
		%this.index[%this.item[%i]] = %i;
	}

	%this.item[%i] = "";
	%this.index[%item] = "";

	if (%a < %b)
	{
		%this.a++;
	}
	else
	{
		%this.b--;
	}

	return 1;
}

// anything set::pop
//  Remove and return an arbitrary items from the set.
//  Returns an empty string if empty.

function set::pop(%this)
{
	if (%this.b - %this.a <= 0)
	{
		return "";
	}

	if (%this.b > mAbs(%this.a))
	{
		%index = %this.b-- + 1;
	}
	else
	{
		%index = %this.a++ - 1;
	}

	%item = %this.item[%index];

	%this.index[%item] = "";
	%this.item[%index] = "";

	return %item;
}

// set::clear
//  Removes all items from the set.

function set::clear(%this)
{
	for (%i = %this.a; %i <= %this.b; %i++)
	{
		%this.index[%this.item[%i]] = "";
		%this.item[%i] = "";
	}

	%this.a = 0;
	%this.b = 0;
}

// bool set::isdisjoint(set other)
//  Returns true if the set has no items in common with *other*.
//  Sets are disjoint if and only if their intersection is the empty set.

function set::isdisjoint(%this, %other)
{
	if (%other.class !$= %this.class)
	{
		return -1;
	}

	%a = %this.a > %other.a ? %this.a : %other.a;
	%b = %this.b < %other.b ? %this.b : %other.b;

	if (%b - %a <= 0)
	{
		return 1;
	}

	for (%i = %a; %i <= %b; %i++)
	{
		if (strStr(%this.item[%i], %other.item[%i]) == 0)
		{
			return 0;
		}
	}

	return 1;
}

// bool set::issubset(set other)
//  Test whether every item in the set is in *other*.

function set::issubset(%this, %other)
{
	if (%other.class !$= %this.class)
	{
		return -1;
	}

	if (%other.b - %other.a <= 0)
	{
		return %this.b - %this.a <= 0;
	}

	for (%i = %this.a; %i <= %this.b; %i++)
	{
		if (%other.index[%this.item[%i]] !$= "")
		{
			return 0;
		}
	}

	return 1;
}

// bool set::issuperset(set other)
//  Test whether every item in *other* is in the set.

function set::issuperset(%this, %other)
{
	if (%other.class !$= %this.class)
	{
		return -1;
	}

	if (%this.b - %this.a <= 0)
	{
		return %other.b - %other.a <= 0;
	}

	for (%i = %other.a; %i <= %other.b; %i++)
	{
		if (%this.index[%other.item[%i]] !$= "")
		{
			return 0;
		}
	}

	return 1;
}

// set set::union(set other, ...)
//  Returns a new set with items from the set and all *other*s.
//  The *other* argument can be repeated up to 20 times.

function set::union(%this,
	%a1, %a2, %a3, %a4, %a5, %a6, %a7, %a8, %a9,
	%a10, %a11, %a12, %a13, %a14, %a15, %a16, %a17, %a18, %a19, %a20
)
{
	%set = %this.copy();

	for (%a = 1; %a < 21; %a++)
	{
		%other = %a[%a];

		if (%other.class !$= %this.class)
		{
			continue;
		}

		for (%i = %other.a; %i <= %other.b; %i++)
		{
			if (%set.index[%other.item[%i]] $= "")
			{
				%set.add(%other.item[%i]);
			}
		}
	}

	return %set;
}

// set set::intersection(set other, ...)
//  Returns a new set with items common to the set and all *other*s.
//  The *other* argument can be repeated up to 20 times, for multiple unions.
//
//  Currently implemented with a very inefficient brute-force approach.
//
//  `O(sum(set1, set2, ..., setx)*n*n)`

function set::intersection(%this,
	%a1, %a2, %a3, %a4, %a5, %a6, %a7, %a8, %a9,
	%a10, %a11, %a12, %a13, %a14, %a15, %a16, %a17, %a18, %a19, %a20
)
{
	%a0 = %this;
	%set = set();

	for (%a = 0; %a < 21; %a++)
	{
		%other = %a[%a];

		if (%other.class !$= %this.class)
		{
			continue;
		}

		for (%i = %other.a; %i <= %other.b; %i++)
		{
			for (%b = 0; %b < 21; %b++)
			{
				if (%b == %a)
				{
					continue;
				}

				if (%a[%b].index[%other.item[%i]] $= "")
				{
					break;
				}
			}

			if (%b == 21)
			{
				%set.add(%other.item[%i]);
			}
		}
	}

	return %set;
}

// set set::difference(set other, ...)
//  Returns a new set with items in the set that are not in the *other*s.
//  The *other* argument can be repeated up to 20 times.

function set::difference(%this,
	%a1, %a2, %a3, %a4, %a5, %a6, %a7, %a8, %a9,
	%a10, %a11, %a12, %a13, %a14, %a15, %a16, %a17, %a18, %a19, %a20
)
{
	%set = set();

	for (%i = %this.a; %i <= %this.b; %i++)
	{
		for (%a = 1; %a < 21; %a++)
		{
			%other = %a[%a];

			if (%other.class !$= %this.class)
			{
				continue;
			}

			for (%j = %other.a; %j <= %other.b; %j++)
			{
				if (%other.index[%this.item[%i]] !$= "")
				{
					break;
				}
			}

			if (%j > %other.b)
			{
				%set.add(%this.item[%i]);
			}
		}
	}

	return %set;
}

// set set::symmetric_difference(set other)
//  Returns a new set with items in either the set or *other* but not both.

function set::symmetric_difference(%this, %other)
{
	%set = set();

	if (%other.class !$= %this.class)
	{
		return %set;
	}

	for (%i = %this.a; %i <= %this.b; %i++)
	{
		if (%other.index[%this.item[%i]] $= "")
		{
			%set.add(%this.item[%i]);
		}
	}

	for (%i = %other.a; %i <= %other.b; %i++)
	{
		if (%this.index[%other.item[%i]] $= "")
		{
			%set.add(%other.item[%i]);
		}
	}

	return %set;
}

// set set::copy
//  Returns a new shallow copy of the set.

function set::copy(%this)
{
	%set = set();

	%set.a = %this.a;
	%set.b = %this.b;

	for (%i = %this.a; %i <= %this.b; %i++)
	{
		%set.item[%i] = %this.item[%i];
		%set.index[%item[%i]] = %i;
	}

	return %set;
}

// set::update(set other, ...)
//  Update the set, adding items from all *other*s.
//  The *other* argument can be repeated up to 20 times.

function set::update(%this,
	%a1, %a2, %a3, %a4, %a5, %a6, %a7, %a8, %a9,
	%a10, %a11, %a12, %a13, %a14, %a15, %a16, %a17, %a18, %a19, %a20
)
{
	for (%a = 1; %a < 21; %a++)
	{
		%other = %a[%a];

		if (%other.class !$= %this.class)
		{
			continue;
		}

		for (%i = %other.a; %i <= %other.b; %i++)
		{
			if (%this.index[%other.item[%i]] $= "")
			{
				%this.add(%other.item[%i]);
			}
		}
	}
}

// set::intersection_update(set other, ...)
//  Update the set, keeping only items found in it and all *other*s.
//  The *other* argument can be repeated up to 20 times.
//
//  Not currently functional.

function set::intersection_update(%this,
	%a1, %a2, %a3, %a4, %a5, %a6, %a7, %a8, %a9,
	%a10, %a11, %a12, %a13, %a14, %a15, %a16, %a17, %a18, %a19, %a20
)
{
	return;

	for (%i = %this.a; %i <= %this.b; %i++)
	{
		for (%a = 1; %a < 21; %a++)
		{
			%other = %a[%a];

			if (%other.class !$= %this.class)
			{
				continue;
			}

			if (%other.index[%this.item[%i]] $= "")
			{
				%this.remove(%this.item[%i]);
				break;
			}
		}
	}
}

// set::difference_update(set other, ...)
//  Update the set, removing items found in *other*s.
//  The *other* argument can be repeated up to 20 times.
//
//  Not yet implemented.

function set::difference_update(%this,
	%a1, %a2, %a3, %a4, %a5, %a6, %a7, %a8, %a9,
	%a10, %a11, %a12, %a13, %a14, %a15, %a16, %a17, %a18, %a19, %a20
)
{
	for (%a = 1; %a < 21; %a++)
	{
		%other = %a[%a];

		if (%other.class !$= %this.class)
		{
			continue;
		}

		for (%i = %other.a; %i <= %other.b; %i++)
		{
			if (%this.index[%other.item[%i]] !$= "")
			{
				%this.remove(%other.item[%i]);
			}
		}
	}
}

// set::symmetric_difference_update(set other)
//  Update the set, keeping only items found in either set, but not both.

function set::symmetric_difference_update(%this, %other)
{
	for (%i = %other.a; %i <= %other.b; %i++)
	{
		if (%this.index[%other.item[%i]] !$= "")
		{
			%this.remove(%other.item[%i]);
		}
		else
		{
			%this.add(%other.item[%i]);
		}
	}
}