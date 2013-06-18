function render_stack(stack, sd) {
  sd.contents().remove();
  stack_item(stack, sd);
}

function stack_item(stack, list) {
  if (stack.length == 0) { return; };
  display_item(stack[0], list);
  stack_item(stack[1], list);
}

function display_item(item, list) {
  if (_.isArray(item)) {
    var li = $('<li></li>');
    list.append(li);
    display_array(item, li);
  } else if (_.isString(item)) {
    list.append('<li>&quot;' + item + '&quot;');
  } else if (_.isObject(item) && !_.isUndefined(item.name)) {
    list.append('<li>' + item.name + '()');
  } else {
    list.append('<li>' + item);
  }
}

function display_array(A, list) {
  var d = $('<ul></ul>');
  _.each(A, function(item) { return display_item(item, d); });
  list.append(d);
}


