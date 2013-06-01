<?php

class Post extends CI_Controller {

    public function __construct() {
        parent::__construct();
        $this->load->model('post_model');
    }

    public function index() {
        $data['post'] = $this->post_model->get_post();
        $data['title'] = 'All posts';
        $this->load->view('templates/header', $data);
        $this->load->view('post/index', $data);
        $this->load->view('templates/footer');
    }

    public function view($id) {
        
        $data['item'] = $this->post_model->get_post($id);

        if (empty($data['item'])) {
            show_404();
        }

        $data['title'] = $data['item']['title'];

        $this->load->view('templates/header', $data);
        $this->load->view('post/view', $data);
        $this->load->view('templates/footer');
    }

}
