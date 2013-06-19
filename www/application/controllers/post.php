<?php

class Post extends CI_Controller {

    public function __construct() {
        parent::__construct();
        $this->load->model('post_model');
        $this->load->model('tag_model');
    }

    public function index() {
        $all_posts = $this->post_model->get_post();
        foreach($all_posts as &$post) {
            $this->my_time_format($post['date_posted']);
        }
        $data['post'] = $all_posts;
        $data['title'] = 'All posts';$data['linkid'] = 'pstlink';
        $this->load->view('templates/header', $data);
        $this->load->view('post/index', $data);
        $this->load->view('templates/footer');
    }

    public function view($id) {

        $data['item'] = $this->post_model->get_post($id);
        $data['tags'] = $this->tag_model->get_all_tags_to_post($id);

        if (empty($data['item'])) {
            show_404();
        }

        $data['title'] = $data['item']['title'];

        $this->load->view('templates/header', $data);
        $this->load->view('post/view', $data);
        $this->load->view('templates/footer');
    }

    public function add() {
        $this->load->helper('form');
        $this->load->library('form_validation');
        $this->load->helper('url');
        
        $data['title'] = 'Add new post';

        $this->form_validation->set_rules('title', 'title', 'required');
        $this->form_validation->set_rules('text', 'text', 'required');

        if ($this->form_validation->run() === FALSE) {
            $this->load->view('templates/header', $data);
            $this->load->view('post/add');
            $this->load->view('templates/footer');
        } else {
            $this->post_model->set_post();
            redirect('/');
        }
    }

    private function my_time_format(&$time)
    {
        $this->load->helper('date');
        $unix = mysql_to_unix($time);
        $mval = "%m";
        $monthNum = mdate($mval, $unix);
        $monthName = date("F", mktime(0, 0, 0, $monthNum, 10));
        $datestring = "%d ".$monthName.", %Y";
        $time = mdate($datestring, $unix);
    }
}
