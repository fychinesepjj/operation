(function($, global){

    $(document).ready(function() {
        function message_user(message, types){
            var types = types || 'grp-info'
            var message_list = $('.grp-messagelist');
            if(message_list.length){
                var message_box = message_list[0];
                $(message_box).empty();
                $(message_box).append('<li class="'+ types +'">'+ message +'</li>')
            }
            else{
                $('#grp-content').prepend('<ul class="grp-messagelist"><li class="'+ types +'">'+ message + '</li></ul>');
            }
        }

        function do_action(action, text){
            if(confirm('确定执行所选<'+ text +'>操作？')){
                $('select[name=action] option[selected]').attr('selected', '');
                $('select[name=action] option[value='+action+']').attr('selected', 'selected');
                $('#grp-changelist-form').submit();
            }
        }
        global.message_user = message_user;
        global.do_action = do_action;

        function fix_actions(){
            var actions_html_list = [];
            var actions = $('select[name=action] option:gt(0)');
            if (actions&&actions.length<=8) { // Only do this for short lists.
                $('div.grp-changelist-actions > *').hide();
                $('select[name=action] option:gt(0)').each(function(i) {
                    actions_html_list.push('<a href="javascript:void(0);" class="action_link bg-normal '+ this.value +'" onclick="do_action(\''+this.value+'\',\''+this.text+'\');">'+this.text+'</a>');
                });
                $('div.grp-changelist-actions').append(actions_html_list.join(''));
            }
        }
         fix_actions();
    });
})(grp.jQuery, window);
